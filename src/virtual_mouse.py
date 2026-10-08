import cv2
import numpy as np
import wx
from pynput.mouse import Button, Controller

# Initialize mouse controller
mouse = Controller()

# Get screen resolution
app = wx.App(False)
(screen_width, screen_height) = wx.GetDisplaySize()

# Camera capture size
capture_width, capture_height = 700, 500

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, capture_width)
cap.set(4, capture_height)

# Morphological kernels
kernel_open = np.ones((5, 5), np.uint8)
kernel_close = np.ones((20, 20), np.uint8)

# HSV range for YELLOW color
lower_bound = np.array([20, 120, 120])
upper_bound = np.array([35, 255, 255])

mouse_pressed = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask yellow color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Remove noise
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

    # Find contours (OpenCV 4+)
    contours, _ = cv2.findContours(
        mask_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        # Extreme points
        left = tuple(largest_contour[largest_contour[:, :, 0].argmin()][0])
        right = tuple(largest_contour[largest_contour[:, :, 0].argmax()][0])
        top = tuple(largest_contour[largest_contour[:, :, 1].argmin()][0])
        bottom = tuple(largest_contour[largest_contour[:, :, 1].argmax()][0])

        # Center
        center_x = int((left[0] + right[0]) / 2)
        center_y = int((top[1] + bottom[1]) / 2)

        # Draw visuals
        cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 7, (255, 0, 0), -1)

        # Map to screen
        screen_x = screen_width - (center_x * screen_width / capture_width)
        screen_y = center_y * screen_height / capture_height
        mouse.position = (screen_x, screen_y)

        # Gesture logic
        if 8000 < area < 18000:  # Open hand
            if mouse_pressed:
                mouse.release(Button.left)
                mouse_pressed = False

        elif 2000 < area < 7000:  # Closed hand
            if not mouse_pressed:
                mouse.press(Button.left)
                mouse_pressed = True

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
