# Virtual Mouse Using OpenCV 🖱️

A computer vision based virtual mouse that allows users to control the system mouse
using hand gestures captured through a webcam.

---

## 🚀 Features
- Real-time hand tracking using color segmentation
- Mouse movement using hand position
- Left-click using hand gesture
- No additional hardware required
- Uses OpenCV and Python

---

## 🛠️ Technologies Used
- Python
- OpenCV
- NumPy
- wxPython
- pynput

---

## 🧠 How It Works
1. Webcam captures video frames
2. Yellow colored hand/object is segmented using HSV
3. Largest contour is detected as hand
4. Hand center controls mouse movement
5. Contour area determines click action

---

## 🖥️ Installation

```bash
git clone https://github.com/your-username/Virtual-Mouse-Using-OpenCV.git
cd Virtual-Mouse-Using-OpenCV
pip install -r requirements.txt
