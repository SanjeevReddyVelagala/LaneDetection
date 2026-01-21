# Real-Time Lane Detection Using OpenCV

A real-time lane detection system built with classical computer vision techniques, inspired by perception pipelines used in autonomous driving systems.

---

## Demo
Provided as demo.mp4

---

## Overview
This project detects **left and right lane boundaries** from a live webcam feed using OpenCV. It applies image preprocessing, edge detection, and line estimation techniques to robustly identify lane markings in real time.

The project focuses on understanding **vision-based lane perception**, a core component of autonomous vehicle safety and driver-assistance systems.

---

## Approach Summary
1. Capture live video from webcam  
2. Apply trapezoidal Region of Interest (ROI) masking  
3. Enhance contrast using CLAHE  
4. Isolate lane colors using HSV thresholding  
5. Detect edges with adaptive Canny edge detection  
6. Extract lane lines using Probabilistic Hough Transform  
7. Filter, average, and draw stable left/right lane lines  

---

## Technical Details

### Region of Interest (ROI)
A trapezoidal mask is applied to focus processing on the road area, reducing noise from irrelevant regions such as the sky or surroundings.

### Contrast Enhancement
CLAHE (Contrast Limited Adaptive Histogram Equalization) is applied to the L-channel in LAB color space to improve lane visibility under varying lighting conditions.

### Color Thresholding
HSV thresholding is used to isolate bright lane markings such as white or light-colored lanes.

### Edge Detection
Canny edge detection is applied using adaptive thresholds based on the median pixel intensity, making the pipeline more robust to lighting changes.

### Line Detection
The Probabilistic Hough Line Transform is used to detect candidate lane segments from the edge-detected image.

### Lane Filtering & Averaging
- Lines are filtered by slope magnitude and image position  
- Outliers are removed using percentile trimming  
- Remaining slopes and intercepts are averaged to produce stable lane lines  

---

## Requirements

### Hardware
- **1080p (1920×1080) camera required**
- The Region of Interest (ROI) mask and lane calculations are hardcoded for 1080p resolution
- Using a lower resolution camera will require modifying ROI coordinates and image dimensions

### Software
- Python 3.x  
- OpenCV  
- NumPy  

---

## How to Run
python lane_detection.py

### Install Dependencies
```bash
pip install opencv-python numpy