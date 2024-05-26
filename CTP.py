import tkinter as tk
from tkinter import filedialog
import pandas as pd
import time
import matplotlib.pyplot as plt
import io
from pandas import DataFrame

from PIL import Image, ImageTk

data= pd.DataFrame()
global a
global b
a=1/50
b=0.2

class DataVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Visualization App")
        
        self.load_button = tk.Button(master, text="Load Data", command=lambda: (self.load_data(),self.display_chart()))
        self.load_button.pack(pady=10)

        self.load_button = tk.Button(master, text="Calibrate Sensor", command=lambda: self.display_chart(1/50))
        self.load_button.pack(pady=10)
        
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()
    
    
    def display_chart(self, adjustment: int = 1):
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))  # Create the figure outside the loop
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('VRVT190 - indukcyjny')
        plt.tight_layout()

        self.data['y'] = self.data['y']*adjustment

        self.ylimits = (self.data['y'].min(), self.data['y'].max() + self.data['y'].std())
        i = 0
        while True:
            buffer.truncate(0)  # Clear the buffer
            buffer.seek(0)  # Reset the buffer position
            self.compose_chart(self.data[i:(i + 100)], buffer, adjustment=adjustment)
            self.canvas.update()  # Update the canvas immediately
            time.sleep(0.05)  # Sleep for a short interval
            i=i+5
            i=i%(len(self.data) - 100)
        
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

    def compose_chart(self, data: DataFrame, buffer, adjustment: int = 1):
        self.canvas.delete("all")  # Clear canvas
        plt.clf()
        plt.plot(data['x'], data['y'])
        plt.ylim(self.ylimits[0], self.ylimits[1])
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image = Image.open(buffer)
        tk_image = ImageTk.PhotoImage(image)
        self.chart_image = tk_image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.chart_image)

def main():
    root = tk.Tk()
    DataVisualizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

