import os
import csv
import cv2
import time
import shutil
import numpy as np
from tflite_runtime.interpreter import Interpreter

name = input("input name : ")

blink1D = []
blink2D = [[0] * 50 for _ in range(20)]
blink = []

total_elapsed_time = 0
prev_frame_time = 0
new_frame_time = 0
blink_row = 0
rep = 0

start_blink = None
status = False

path = 'source/capture'
path_csv = 'source/timeBlink'
path_save = f"source/backup/{name}"

size_font = 0.35
font = cv2.FONT_HERSHEY_SIMPLEX

interpreter = Interpreter(model_path="model/model_EBlink_optimize.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def update_2d_array():
    global blink1D, blink2D, blink_row
    for i in range(min(len(blink1D), len(blink2D[0]))):
        blink2D[blink_row][i] = blink1D[i]
    blink1D = []
    blink_row = (blink_row + 1) % 20

    with open('source/timeBlink/data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(blink2D)


def preprocess_frame(frame):
    normalized_frame = frame / 255.0
    preprocessed_frame = np.expand_dims(normalized_frame.astype(np.float32), axis=0)
    return preprocessed_frame


def classify_frame(frame):
    preprocessed_frame = preprocess_frame(frame)
    interpreter.set_tensor(input_details[0]['index'], preprocessed_frame)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    class_label = "open" if output_data <= 0.5 else "close"
    return class_label, output_data


# Open video capture
cap = cv2.VideoCapture(0)

if not os.path.exists(path):
    os.makedirs(path)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_file = os.path.join(path, f"{name}.mp4")
output = cv2.VideoWriter(output_file, fourcc, 30, (224, 224))

timer_now = time.time()
last_time = timer_now

try:
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        total_elapsed_time = time.time() - last_time
        if total_elapsed_time >= 60:
            cek_blink = len(blink1D)
            if cek_blink <= 10:  # cek status cvs
                status = True
            else:
                status = False

            update_2d_array()
            print("2D Array after storing:", blink2D)
            rep += 1
            last_time = time.time()

        frame = cv2.resize(frame, (input_details[0]['shape'][2], input_details[0]['shape'][1]))
        class_label, output_data = classify_frame(frame)

        if class_label == "close":
            start_blink = time.time()

        elif class_label == "open":
            if start_blink is not None:
                blinkDur = time.time() - start_blink
                blink1D.append(blinkDur)
                start_blink = None

        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = str(int(fps))

        # Display prediction result on the frame
        cv2.rectangle(frame, (0, 0), (224, 30), (255, 255, 255), -1)
        cv2.putText(frame, f"{'csv' if status else 'normal'}", (180, 25), font, size_font, (0, 0, 0), 1)
        cv2.putText(frame, f"status:{class_label}{output_data}", (0, 10), font, size_font, (0, 0, 0), 1)
        cv2.putText(frame, f"time:{total_elapsed_time:.2f}s => {rep}m", (0, 25), font, size_font, (0, 0, 0), 1)
        cv2.putText(frame, f'fps:{fps}', (180, 10), font, size_font, (0, 0, 0), 1)

        output.write(frame)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    output.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"An error occured : {e}")

if not os.path.exists(path_save):
    os.makedirs(path_save)

addFile_video = os.listdir(path)
addFile_csv = os.listdir(csv)

for video in addFile_video:
    src_path = os.path.join(path, video)
    des_path = os.path.join(path_save, video)
    shutil.move(src_path, des_path)

for csv in addFile_csv:
    src_path = os.path.join(path_csv, csv)
    des_path = os.path.join(path_save, csv)
    shutil.move(src_path, des_path)

directory = "source/timeBlink"
os.makedirs(directory, exist_ok=True)
csv_file = os.path.join(directory, "data.csv")
with open(csv_file, "w") as file:
    pass

os.system("python3 run.py")
