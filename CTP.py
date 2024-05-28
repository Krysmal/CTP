from copy import copy
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import time
import matplotlib.pyplot as plt
import io
from pandas import DataFrame

from PIL import Image, ImageTk

global a
global b
a=1/50
b=0.2

class DataVisualizationApp:
    data: DataFrame

    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("CTP MALINOWSKI")
        self.master.geometry("900x600")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()
        
        self.load_button = tk.Button(self.button_frame, text="Load Data", command=lambda: (self.load_data(),self.display_chart(data=self.data, canvas=self.canvas, y_label='Milimeters [mm]')), width=102)
        self.load_button.grid(row=0, column=0, columnspan=2)

        self.calibrate_button = tk.Button(self.button_frame, text="Calibrate Sensor", command=lambda: self.display_chart(data=copy(self.data),canvas=self.canvas, adjustment=1/50, y_label='Volt [V]'), width=50)
        self.calibrate_button.grid(row=1,column=0)

        self.count_impulses_button = tk.Button(self.button_frame, text="Count impulses", command=lambda: self.count_signals_button_callback(), width=50)
        self.count_impulses_button.grid(row=1, column=1)

        self.velocity_button = tk.Button(self.button_frame, text="Velocity", command=lambda: self.derivative_function_callback(1, color='yellow'), width=50)
        self.velocity_button.grid(row=2, column=0)

        self.velocity_button = tk.Button(self.button_frame, text="Acceleration", command=lambda: self.derivative_function_callback(2,name='Acceleration',color='red'), width=50)
        self.velocity_button.grid(row=2, column=1)
        
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()
    
    def display_chart(self, data: DataFrame, canvas,  adjustment: int = 1, color: str = 'blue', y_label: str = 'Y'):
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))
        data['y'] = data['y']*adjustment


        self.ylimits = (data['y'].min(), data['y'].max() + data['y'].std())
        i = 0
        while True:
            buffer.truncate(0)
            buffer.seek(0) 
            self.compose_chart(data[i:(i + 100)], buffer, canvas, color, y_label)
            canvas.update()
            time.sleep(0.05)
            i=i+5
            i=i%(len(data) - 100)
        
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)

    def compose_chart(self, data: DataFrame, buffer, canvas, color, y_label):
        canvas.delete("all")
        plt.clf()
        plt.xlabel('Time [s]')
        plt.ylabel(y_label)
        plt.title('VRVT190 - indukcyjny')
        plt.tight_layout()
        plt.plot(data['x'], data['y'], color=color)
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
        self.display_chart(self.tempData, self.canvas, y_label='Impulses per second')

    def derivative_function_callback(self, derivative_degree: int = 1, name: str = 'Velocity', color: str = 'blue') -> None:
       derivedData = self.data.copy()
       i = 0
       while i < derivative_degree:
        derivedData['y'] = derivedData['y'].diff()/derivedData['x'].diff()
        i = i + 1
       self.display_chart(derivedData, self.canvas, color=color, y_label=name)

def main():
    root = tk.Tk()
    DataVisualizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

