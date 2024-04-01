import os
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BlinkAnalyzer:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def count(self, row_index):
        with open(self.csv_filename, 'r') as file:
            reader = csv.reader(file)
            for row_number, row in enumerate(reader):
                if row_number == row_index:
                    values = [float(value) for value in row if value != '0']
                    blink = len(values)
                    return values, blink
        return None

    def visualize(self, minute):
        blink = []
        value = []
        timeBlink1D = []

        for i in range(minute):
            row_index = i
            values, blinks = self.count(row_index)
            if values is not None:
                blink.append(blinks)
                value.append(values)
                print(f"Non-zero values in row {row_index}: {values}")
            else:
                print("Row not found or contains only zeros.")

        print(blink)
        print(value)

        timeBlink1D = [time for sublist in value for time in sublist]

        return timeBlink1D, blink, value


class show_graph:
    def __init__(self, root):
        self.root = root
        self.canvas = None

    def plot_data(self, analyzer, minute):
        timeBlink1D, blink, value = analyzer.visualize(minute)

        # Calculate figure size in inches based on the screen size and desired DPI
        screen_width_px = 680
        screen_height_px = 300
        desired_dpi = 100  # You can adjust this value as needed
        screen_width_in = screen_width_px / desired_dpi
        screen_height_in = screen_height_px / desired_dpi

        fig = plt.figure(figsize=(screen_width_in, screen_height_in), dpi=desired_dpi)

        # Plot for blink counts
        plt.subplot(1, 2, 1)
        plt.plot(blink)
        plt.xlabel('Time (minute)')
        plt.ylabel('Blink')
        plt.title('Blink Count')

        # Plot for timeBlink1D
        plt.subplot(1, 2, 2)
        plt.plot(timeBlink1D)
        plt.xlabel('Blink')
        plt.ylabel('Time (ms)')
        plt.title('Blink Count')

        plt.tight_layout()

        # Create a canvas to display the figure
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, columnspan=2, padx=5, pady=5, sticky='ew')

    def main(self):
        self.root.destroy()
        os.system("python3 run.py")


def main():
    root = tk.Tk()
    root.title("Blink Analyzer")

    analyzer = BlinkAnalyzer('source/timeBlink/data.csv')

    minute_label = ttk.Label(root, text="Enter minute:")
    minute_label.grid(row=0, column=0, padx=5, pady=5)

    minute_entry = ttk.Entry(root)
    minute_entry.grid(row=0, column=1, padx=5, pady=5)

    def plot():
        minute = int(minute_entry.get())
        fig = show_graph(root).plot_data(analyzer, minute)
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, columnspan=2, padx=5, pady=5)

    plot_button = ttk.Button(root, text="Plot", command=plot)
    plot_button.grid(row=2, columnspan=2, padx=5, pady=5, sticky='ew')

    plot_button = ttk.Button(root, text="back", command=show_graph(root).main)
    plot_button.grid(row=3, columnspan=2, padx=5, pady=5, sticky='ew')

    root.mainloop()


if __name__ == '__main__':
    main()

