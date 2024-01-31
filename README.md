# Time-Series-Visualizer

### Technical Summary of the Software

**Software Name**: Time Series Visualizer (TSV)

**Purpose**: The Time Series Visualizer is a graphical user interface (GUI) application designed to synchronize video playback with corresponding time-series data visualization. It is particularly useful for applications where video frames need to be analyzed alongside quantitative data, such as in sports analytics, scientific experiments, or any field where video observations are coupled with sensor or numerical data.

**Core Features**:
1. **Video Playback**: Plays MP4 and MOV video files, with a dedicated area for video display.
2. **Data Visualization**: Plots time-series data from CSV files on two separate graphs located below the video frame.
3. **Synchronization**: Includes a scrollbar that synchronizes the video frame with the corresponding points in the data graphs.
4. **Statistics Display**: A sidebar that shows the current frame number and corresponding x, y data points from both graphs.
5. **Customizable Interface**: Features like adjustable window size, colors, and a resizable video frame to fit different screen sizes and preferences.

### How to Use the Software

1. **Opening a Video**: Click the "Load Video" button to select and load a video file. The video will appear in the designated frame.
2. **Loading Data**: Use the "Load Data for Graph 1" and "Load Data for Graph 2" buttons to load corresponding CSV files. The first two columns of these files will be used as x and y values for the graphs.
3. **Synchronization**: Drag the scrollbar at the bottom to navigate through the video. As you move the scrollbar, the video frames and the vertical lines on the graphs will update accordingly, showing the corresponding data points.
4. **Viewing Statistics**: The statistics panel will dynamically update to show the current video frame number and data points from both graphs.

### Limitations

- **File Formats**: Limited to MP4 and MOV for videos, and CSV for data files.
- **Performance**: Large video files or extensive data may lead to performance issues, depending on the computer's processing power.
- **Synchronization**: Assumes a direct correlation between frame numbers and data points. Any mismatch in the frequency of data collection between the video and CSV files may lead to inaccurate synchronization.
- **Data Visualization**: Limited to plotting two-dimensional data (x, y) from CSV files. More complex or multi-dimensional data types are not supported.

### Setup Guide and Required Resources

**System Requirements**:
- **Operating System**: Any OS that supports Python and its libraries (Windows, macOS, Linux).
- **Python Version**: Python 3.x.

**Dependencies**:
- **Tkinter**: Python's standard GUI toolkit, usually comes pre-installed with Python.
- **Pandas**: For handling CSV files. Install via pip (`pip install pandas`).
- **Matplotlib**: For plotting graphs. Install via pip (`pip install matplotlib`).
- **OpenCV**: For handling video playback. Install via pip (`pip install opencv-python`).
- **Pillow (PIL)**: For image processing. Install via pip (`pip install Pillow`).

**Installation Steps**:
1. Ensure Python 3.x is installed.
2. Install required Python libraries using pip (if not already installed).
3. Run the Python script to start the application.

**Usage**:
- Launch the script to open the GUI.
- Use the interface buttons to load video and data files.
- Use the scrollbar for synchronization and interaction.

This software is suitable for small to medium-scale analysis tasks where video and time-series data synchronization is required. For larger, more complex applications, additional optimization and feature enhancements would be necessary.
