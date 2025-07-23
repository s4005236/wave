import cv2 as cv
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerOptions


def initialize_mediapipe_hands(model_path_hand):
    """
    Defines the different settings to mark the different parts of the hands
    """
    options = HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path_hand),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )
    hand_landmarker = HandLandmarker.create_from_options(options)
    return hand_landmarker

def initialize_mediapipe_gestures(model_path_gestures):
    """
    Defines the different settings to recognize gestures
    """
    gestures_options = vision.GestureRecognizerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=model_path_gestures),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )
    gestures_recognizer = vision.GestureRecognizer.create_from_options(gestures_options)
    return gestures_recognizer

def mark_hands():
    """
    Marks the hands in the video stream using mediapipe hand landmarker
    """
    model_path_hand = "mediapipe_models\\hand_landmarker.task"
    hand_landmarker = initialize_mediapipe_hands(model_path_hand)

    cap = cv.VideoCapture(1)
    timestamp = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results = hand_landmarker.detect_for_video(mp_image, timestamp)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                for landmark in hand_landmarks:
                    x_px = int(landmark.x * frame.shape[1])
                    y_px = int(landmark.y * frame.shape[0])
                    cv.circle(frame, (x_px, y_px), 5, (0, 255, 0), -1)

        flipped_frame = cv.flip(frame, 1)
        cv.imshow("WAVE Hand Tracking", flipped_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

        timestamp += int(1000 / cap.get(cv.CAP_PROP_FPS))

    cap.release()
    cv.destroyAllWindows

def recognize_gestures():
    """
    Recognizes gestures using the mediapipe gesture recognizer
    """
    model_path_gestures = "mediapipe_models\\gesture_recognizer.task"
    gestures_recognizer = initialize_mediapipe_gestures(model_path_gestures)

    cap = cv.VideoCapture(1)
    timestamp = 1000

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results = gestures_recognizer.recognize_for_video(mp_image, timestamp)

        if results.gestures:
            for gesture in results.gestures:
                print(f"Recognized gesture: {gesture[0].category_name}")

        flipped_frame = cv.flip(frame, 1)
        cv.imshow("WAVE Gesture Recognition", flipped_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

        timestamp += int(1000 / cap.get(cv.CAP_PROP_FPS))

    cap.release()
    cv.destroyAllWindows()


def main():
    """
    Executes the functions in the right order
    """
    recognize_gestures()


if __name__ == "__main__":
    main()
