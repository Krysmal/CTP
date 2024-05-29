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

class MalinButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        kwargs['bg'] = kwargs.get('bg', '#333333')
        kwargs['fg'] = kwargs.get('fg', '#FFFFFF')
        kwargs['width'] = kwargs.get('width', 30)
        super().__init__(master, **kwargs)

class DataVisualizationApp:
    data: DataFrame
    stop_chart: bool = False
    buttons: list[MalinButton]

    def __init__(self, master: tk.Tk):
        self.master = master
        self.initView(master)

    def initView(self, master):
        self.master.title("CTP MALINOWSKI, KUŚ, PALUCH, KURC")
        self.master.geometry("900x440")
        self.master.configure(background='#272640')

        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=0, column=0, sticky='n', pady=10)
        self.button_frame.configure(background='#272640', height=400)

        self.buttons = []

        self.initButtons(self.button_frame)

        self.read_value_label = tk.Label(self.button_frame, text="Wartość w połowie wykresu:", font=('', 12), background='#272640', fg='white')
        self.read_value_label.grid(row=5, column=0)

        self.read_value = tk.Label(self.button_frame, text="", font=('', 16), background='#272640', fg='white')
        self.read_value.grid(row=6, column=0)
        
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.configure(background='#272640')
        self.canvas.grid(row=0, column=1, pady=20, padx=10)

    def initButtons(self, root):
        self.load_button = MalinButton(root, text="Load Data", command=lambda: (self.load_data(),self.set_current_color_label_unit('blue','Milimeters [mm]','[mm]'),self.display_chart(data=self.data)))
        self.load_button.grid(row=0, column=0, sticky='n', padx=10, pady=10,)

        self.calibrate_button = MalinButton(root, text="Calibrate Sensor", command=lambda: (self.set_current_color_label_unit('blue','Volt [V]','[V]'), self.display_chart(data=copy(self.data), adjustment=1/50)))
        self.calibrate_button.grid(row=1,column=0, sticky='n', padx=10, pady=10,)

        self.count_impulses_button = MalinButton(root, text="Count impulses", command=lambda: self.count_signals_button_callback())
        self.count_impulses_button.grid(row=2, column=0, sticky='n', padx=10, pady=10,)

        self.velocity_button = MalinButton(root, text="Velocity", command=lambda: self.derivative_function_callback(1, color='green'))
        self.velocity_button.grid(row=3, column=0, sticky='n', padx=10, pady=10,)

        self.acceleration_button = MalinButton(root, text="Acceleration", command=lambda: self.derivative_function_callback(2,name='Acceleration [mm/s^2]',color='red'))
        self.acceleration_button.grid(row=4, column=0, sticky='n', padx=10, pady=10,)

        self.start_button = MalinButton(root, text="Start/Stop", command=self.toggle_start)
        self.start_button.grid(row=7, column=0, sticky='n', padx=10, pady=10,)

        self.move_button_frame = tk.Frame(root)
        self.move_button_frame.grid(row=8, column=0, sticky='n', pady=10)
        self.move_button_frame.configure(background='#272640')

        self.left_button = MalinButton(self.move_button_frame, text="Move left", command=self.move_left, width=13)
        self.left_button.grid(row=0, column=0, sticky='n', padx=5, pady=10,)

        self.right_button = MalinButton(self.move_button_frame, text="Move right", command=self.move_right, width=13)
        self.right_button.grid(row=0, column=1, sticky='n', padx=5, pady=10,)

        self.index = 0

        self.buttons.append(self.load_button)
        self.buttons.append(self.calibrate_button)
        self.buttons.append(self.velocity_button)
        self.buttons.append(self.count_impulses_button)
        self.buttons.append(self.acceleration_button)
        self.buttons.append(self.start_button)
        self.buttons.append(self.left_button)
        self.buttons.append(self.right_button)

        self.disable_buttons()

    def move_left(self):
        self.index = max(0, self.index - 50)
        self.refresh_chart()
    
    def move_right(self):
        self.index = min(len(self.data), self.index + 50)
        self.refresh_chart()

    def refresh_chart(self):
        stop_chart_on_call = self.stop_chart
        self.stop_chart = False
        self.update_chart()
        self.stop_chart = stop_chart_on_call

    def toggle_start(self):
        if self.stop_chart == True:
            self.stop_chart = False
        else:
            self.stop_chart = True

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        self.load_button.config(state=tk.NORMAL)
    
    def display_chart(self, data: DataFrame, adjustment: int = 1):
        self.stop_chart = False
        self.buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))
        data['y'] = data['y']*adjustment


        self.ylimits = (data['y'].min(), data['y'].max() + data['y'].std())
        while True:
            self.update_chart()

    def update_chart(self):
        self.buffer.truncate(0)
        self.buffer.seek(0) 
        if self.stop_chart == False:
            self.sent_data = self.data[self.index:(self.index + 100)]
            self.compose_chart(self.sent_data)
            self.index=self.index+5
            self.index=self.index%(len(self.data) - 100)
        self.canvas.update()
        time.sleep(0.05)

    def set_current_color_label_unit(self, color, label, unit):
        self.color = color
        self.y_label = label
        self.unit = unit

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.enable_buttons()

    def compose_chart(self, data: DataFrame):
        self.canvas.delete("all")
        plt.clf()
        plt.xlabel('Time [s]')
        plt.ylabel(self.y_label)
        plt.title('VRVT190 - indukcyjny')
        plt.tight_layout()
        plt.plot(data['x'], data['y'], color=self.color)
        center_x = (data['x'].min() + data['x'].max()) / 2
        plt.axvline(x=center_x, color='g', linestyle='--', label='Środek')
        plt.ylim(self.ylimits[0], self.ylimits[1])
        plt.savefig(self.buffer, format="png")
        self.buffer.seek(0)
        image = Image.open(self.buffer)
        tk_image = ImageTk.PhotoImage(image)
        self.chart_image = tk_image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.chart_image)
        rounded_value = round(data.iloc[50]['y'], 3)
        self.updateLabel(f'{rounded_value} {self.unit}')

    def updateLabel(self, new_value: str):
        self.read_value.configure(text=new_value)

    def count_signals_in_range(self, range:(int,int)) -> int:
        self.tempData.append((range[0],float((self.data[(self.data['x'] >= range[0]) & (self.data['x'] < range[1])]['x'].count()))/0.05))

    
    def count_signals_button_callback(self) -> None:
        self.tempData = []
        i = self.data.min()[0]
        while i < self.data.max()[0]:
            self.count_signals_in_range((i, i+0.05))
            i = i + 0.05
        self.tempData = DataFrame(self.tempData, columns=['x', 'y'])
        self.set_current_color_label_unit('blue','Impulses per second','[Impulses/s]')
        self.display_chart(self.tempData)

    def derivative_function_callback(self, derivative_degree: int = 1, name: str = 'Velocity [mm/s]', color: str = 'blue') -> None:
       derivedData = self.data.copy()
       i = 0
       while i < derivative_degree:
        derivedData['y'] = derivedData['y'].diff()/derivedData['x'].diff()
        i = i + 1
       self.set_current_color_label_unit(color,name,f'[mm/s^{derivative_degree}]')
       self.display_chart(derivedData)

def main():
    root = tk.Tk()
    DataVisualizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

