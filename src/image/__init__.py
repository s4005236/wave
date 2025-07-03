import cv2 as cv
import numpy as np


def start_camera():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Cannot receive frame. Exiting...")
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow("WAVE Camera Module", gray)

        if cv.waitKey(1) == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


def main():
    start_camera()


if __name__ == "__main__":
    main()
