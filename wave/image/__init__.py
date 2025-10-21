import time

import cv2
from picamera2 import Picamera2

picam = Picamera2()
# size doesn't have to be in there, at least it's not working for my setup when I change the values
# default is 640 x 480
config = picam.configure(
    picam.create_preview_configuration(main={"size": (640, 480)})
)
picam.start()
time.sleep(1)

while True:
    frame = picam.capture_array()
    gray = cv2.cvtColor(
        frame, cv2.COLOR_BGR2GRAY
    )  # Grayscale, 0–255 for every pixel
    cv2.imshow("wave - testing grayscale", gray)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

picam.close()
cv2.destroyAllWindows()
