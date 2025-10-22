import time

import cv2
from picamera2 import Picamera2

# Configuration
FPS = 10

picam = (
    Picamera2()
)  # is needed to use Raspberry Pi Cameras that are connected via CSI Interface
picam.configure(picam.create_preview_configuration(main={"size": (640, 480)}))
picam.start()
time.sleep(1)

frame_time = 1.0 / FPS  # time between two frames

while True:
    start = time.time()
    frame = picam.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("wave - testing grayscale", gray)

    if cv2.waitKey(1) & 0xFF == ord(
        "q"
    ):  # returns ASCII-Code of the given Key; 0xFF ensures that only the last 8 bits of the actual key are being used
        break

    elapsed = time.time() - start
    delay = max(
        0, frame_time - elapsed
    )  # ensures positive numbers in case the loop needs more time than the fps cap
    time.sleep(delay)  # "dynamic" delay based on the runtime of the loop

picam.close()
cv2.destroyAllWindows()
