import tkinter as tk
from tkinter import filedialog
import pandas as pd
import time
import matplotlib.pyplot as plt
import io

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
        
        self.load_button = tk.Button(master, text="Load Data", command=self.load_data)
        self.load_button.pack(pady=10)

        self.load_button = tk.Button(master, text="Calibrate Sensor", command=self.Calibrate_Sensor)
        self.load_button.pack(pady=10)
        
        self.canvas = tk.Canvas(master, width=600, height=400)
        self.canvas.pack()

    
    
    

    def load_data(self):
        global data
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            
            data = pd.read_csv(file_path)

            buffer = io.BytesIO()
            plt.figure(figsize=(6, 4))  # Create the figure outside the loop
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Data Visualization')
            plt.tight_layout()
            self.ylimits = (data['y'].min(), data['y'].max() + data['y'].std())

            for i in range(0, len(data) - 100, 5):
                buffer.truncate(0)  # Clear the buffer
                buffer.seek(0)  # Reset the buffer position
                self.display_chart(data[i:(i + 100)], buffer)
                self.canvas.update()  # Update the canvas immediately
                time.sleep(0.05)  # Sleep for a short interval

            plt.close()

    def Calibrate_Sensor(self):
        global data
        if data.empty:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                data = pd.read_csv(file_path)
    
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 4))  # Create the figure outside the loop
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Data Visualization')
        plt.tight_layout()
        self.ylimits = (data['y'].min(), (data['y'].max() + data['y'].std())*a)
        for i in range(0, len(data) - 100, 5):
            buffer.truncate(0)  # Clear the buffer
            buffer.seek(0)  # Reset the buffer position
            self.display_chart_v2(data[i:(i + 100)], buffer)
            self.canvas.update()  # Update the canvas immediately
            time.sleep(0.05)  # Sleep for a short interval
        plt.close()
        



    def display_chart(self, data, buffer):
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


    def display_chart_v2(self, data, buffer):
        
        self.canvas.delete("all")  # Clear canvas
        plt.clf()
        plt.plot(data['x'], data['y']*a+b)
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

