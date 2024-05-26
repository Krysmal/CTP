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
    data: DataFrame
    tempData = []

    def __init__(self, master):
        self.master = master
        self.master.title("Data Visualization App")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()
        
        self.load_button = tk.Button(self.button_frame, text="Load Data", command=lambda: (self.load_data(),self.display_chart(self.data, canvas=self.canvas)))
        self.load_button.grid(row=0, column=0, columnspan=2)

        self.calibrate_button = tk.Button(self.button_frame, text="Calibrate Sensor", command=lambda: self.display_chart(self.data,canvas=self.canvas, adjustment=1/50))
        self.calibrate_button.grid(row=1,column=0)

        self.count_impulses_button = tk.Button(self.button_frame, text="Count impulses", command=lambda: self.count_signals_button_callback())
        self.count_impulses_button.grid(row=1, column=1)
        
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

        self.secondChart = tk.Canvas(master, width=600, height=400)
        self.secondChart.pack()
    
    
    def display_chart(self, data: DataFrame, canvas,  adjustment: int = 1):
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('VRVT190 - indukcyjny')
        plt.tight_layout()
        data['y'] = data['y']*adjustment


        self.ylimits = (data['y'].min(), data['y'].max() + data['y'].std())
        i = 0
        while True:
            buffer.truncate(0)
            buffer.seek(0) 
            self.compose_chart(data[i:(i + 100)], buffer, canvas)
            canvas.update()
            time.sleep(0.05)
            i=i+5
            i=i%(len(data) - 100)
        
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

    def compose_chart(self, data: DataFrame, buffer, canvas):
        canvas.delete("all")
        plt.clf()
        plt.plot(data['x'], data['y'])
        plt.ylim(self.ylimits[0], self.ylimits[1])
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image = Image.open(buffer)
        tk_image = ImageTk.PhotoImage(image)
        self.chart_image = tk_image
        canvas.create_image(0, 0, anchor=tk.NW, image=self.chart_image)

    def count_signals_in_range(self, range:(int,int)) -> int:
        self.tempData.append((range[0],float((self.data[(self.data['x'] >= range[0]) & (self.data['x'] < range[1])]['x'].count()))/0.05))

    
    def count_signals_button_callback(self) -> None:
        self.tempData = []
        i = self.data.min()[0]
        while i < self.data.max()[0]:
            self.count_signals_in_range((i, i+0.05))
            i = i + 0.05
        self.tempData = DataFrame(self.tempData, columns=['x', 'y'])
        self.display_chart(self.tempData, self.secondChart)

def main():
    root = tk.Tk()
    DataVisualizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

