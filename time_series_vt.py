import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class VideoGraphApp:

    def __init__(self, window, window_title):
        self.cap = None
        self.video_frame_label = None
        self.graph_data1 = None
        self.graph_data2 = None
        self.window = window
        self.window.title(window_title)

        self.graph_data1 = pd.DataFrame()  
        self.graph_data2 = pd.DataFrame()  

        self.window.geometry("950x900")

        # Define colors
        self.colors = {
            "dark_red": "#FEEFE5",
            "yellow": "#FEEFE5",
            "light_yellow": "#CC3F0C",
            "light_green": "#2A2B2A",
            "green_blue": "#FEEFE5"
        }

        # Styling
        self.window.configure(background=self.colors["light_green"])
        self.padding = {'padx': 5, 'pady': 5}

        # Add Title
        self.title_label = tk.Label(window, text="Time Series Visualization Tool", font=("Times New Roman", 16, "bold"), bg=self.colors["yellow"])
        self.title_label.grid(row=0, column=0, columnspan=4, **self.padding)

        # Video Frame
        self.video_frame = tk.Label(window, bg='black', width=60, height=10)
        self.video_frame.grid(row=1, column=1, columnspan=3, **self.padding)

        # Graphs
        self.figure, self.ax = plt.subplots(2, 1)
        self.figure.subplots_adjust(hspace=0.5)  
        self.canvas = FigureCanvasTkAgg(self.figure, master=window)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=1, columnspan=3, **self.padding)

        # Scale (replaces Scrollbar)
        self.scale = tk.Scale(window, from_=0, to=100, orient='horizontal', command=self.update_scroll, bg=self.colors["green_blue"])
        self.scale.grid(row=3, column=1, columnspan=3, sticky='ew')

        # Load Video Button
        self.btn_load_video = tk.Button(window, text="Load Video", command=self.load_video, bg=self.colors["dark_red"])
        self.btn_load_video.grid(row=1, column=0, **self.padding)

        # Load Graph Data Buttons
        self.btn_load_data1 = tk.Button(window, text="Load Data for Graph 1", command=lambda: self.load_data(0), bg=self.colors["light_yellow"])
        self.btn_load_data1.grid(row=2, column=0, **self.padding)

        self.btn_load_data2 = tk.Button(window, text="Load Data for Graph 2", command=lambda: self.load_data(1), bg=self.colors["light_yellow"])
        self.btn_load_data2.grid(row=3, column=0, **self.padding)

        self.stats_label = tk.Label(window, text="Statistics", bg="#FEEFE5", justify=tk.LEFT, anchor="w")
        self.stats_label.grid(row=3, column=4, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.window.mainloop()

    def load_video(self):
        video_path = filedialog.askopenfilename(title="Select Video File", 
                                                filetypes=(("MP4 files", "*.mp4"), ("MOV files", "*.mov"), ("All files", "*.*")))
        if not video_path:
            return

        self.cap = cv2.VideoCapture(video_path)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.scale.config(to=total_frames - 1)
        self.update_video_frame()

    def load_data(self, graph_index):
        csv_path = filedialog.askopenfilename(title="Select CSV File", 
                                              filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if not csv_path:
            return

        try:
            # Read CSV file with the first row as headers
            data = pd.read_csv(csv_path, header=0)
            
            # Check if there are at least two columns
            if data.shape[1] < 2:
                messagebox.showerror("Error", "CSV file must contain at least two columns")
                return

            # Store the data
            if graph_index == 0:
                self.graph_data1 = data
            else:
                self.graph_data2 = data

            # Update the scale's maximum value
            max_data_length = max(len(self.graph_data1), len(self.graph_data2))
            self.scale.config(to=max_data_length - 1)

            # Update the graphs
            self.update_graphs()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_video_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Resize frame to fit within the GUI dimensions
                desired_width = 400  
                desired_height = 250  
                frame = cv2.resize(frame, (desired_width, desired_height))

                # Convert color and display in Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                image = ImageTk.PhotoImage(image)

                if self.video_frame_label is None:
                    self.video_frame_label = tk.Label(self.video_frame, image=image)
                    self.video_frame_label.image = image
                    self.video_frame_label.pack()
                else:
                    self.video_frame_label.configure(image=image)
                    self.video_frame_label.image = image
            else:
                self.cap.release()

    def update_graphs(self, scroll_position=None):
        for i, ax in enumerate(self.ax):
            graph_data = getattr(self, f'graph_data{i + 1}')
            if not graph_data.empty:
                ax.clear()
                # Set the labels for the x and y axes
                x_label = graph_data.columns[0]
                y_label = graph_data.columns[1]
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.plot(graph_data.iloc[:, 0], graph_data.iloc[:, 1])
                if scroll_position is not None and scroll_position < len(graph_data):
                    ax.axvline(x=graph_data.iloc[scroll_position, 0], color='red')
        self.canvas.draw()

    def update_scroll(self, scroll_position):
        scroll_position = int(float(scroll_position))  
        if self.cap and self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, scroll_position)
            self.update_video_frame()
        self.update_graphs(scroll_position)
        scroll_position = int(float(scroll_position))
        self.update_stats(scroll_position)

    def update_stats(self, frame_number=None):
        stats_text = "Statistics:\n"
        if frame_number is not None:
            stats_text += f"Current Frame: {frame_number}\n"

        # Extract coordinates for Graph 1
        if not self.graph_data1.empty and frame_number < len(self.graph_data1):
            x1, y1 = self.graph_data1.iloc[frame_number, 0:2]
            stats_text += f"Graph 1 - X: {x1}, Y: {y1}\n"
        
        # Extract coordinates for Graph 2
        if not self.graph_data2.empty and frame_number < len(self.graph_data2):
            x2, y2 = self.graph_data2.iloc[frame_number, 0:2]
            stats_text += f"Graph 2 - X: {x2}, Y: {y2}\n"

        self.stats_label.config(text=stats_text)

    

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGraphApp(root, "Time Series Visualizer")
