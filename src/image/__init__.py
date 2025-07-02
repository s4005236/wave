import cv2 as cv
import numpy as np

""" def find_available_camera(max=5):
    for i in range(max):
        cap = cv.VideoCapture(i)
        if cap.read()[0]:   
            cap.release()
            return i
        cap.release()
    return None

camera_index = find_available_camera()

if camera_index is None:
    print("No available camera found.")
    exit() """

cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot receive frame. Exiting...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("frame", gray)
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
