import os
import cv2

print("Review".center(50, "-"))
name = input("Please insert name : ")
dir_video = f"source/backup/{name}.mp4"

try:
    cap = cv2.VideoCapture(dir_video)

    print("press q for quit")

    while True:
        ret, frame = cap.read()
        cv2.imshow(f'video {name}', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"An error occured : {e}")

print()
os.system("python3 run.py")