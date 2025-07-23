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

def mark_hands(hand_landmarker, mp_image, timestamp, frame):
    """
    Marks the hands in the video stream using mediapipe hand landmarker
    """
    results = hand_landmarker.detect_for_video(mp_image, timestamp)

    if results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            for landmark in hand_landmarks:
                x_px = int(landmark.x * frame.shape[1])
                y_px = int(landmark.y * frame.shape[0])
                cv.circle(frame, (x_px, y_px), 5, (0, 255, 0), -1)

def recognize_gestures(gestures_recognizer, mp_image, timestamp, frame):
    """
    Recognizes gestures using the mediapipe gesture recognizer
    """
    results = gestures_recognizer.recognize_for_video(mp_image, timestamp)

    if results.gestures:
        for gesture in results.gestures:
            print(f"Recognized gesture: {gesture[0].category_name}")

def main():
    """
    Main function to initialize mediapipe hand landmarker and gesture recognizer,
    start video capture, and process frames for hand tracking and gesture recognition.
    """
    # Initialize mediapipe hand landmarker and gesture recognizer options
    model_path_hand = "mediapipe_models\\hand_landmarker.task"
    model_path_gestures = "mediapipe_models\\gesture_recognizer.task"
    hand_landmarker = initialize_mediapipe_hands(model_path_hand)
    gestures_recognizer = initialize_mediapipe_gestures(model_path_gestures)

    # Start video capture
    cap = cv.VideoCapture(1)
    timestamp = 0

    # While loop till the video capture ends
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB format for mediapipe processing
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect hands
        mark_hands(hand_landmarker, mp_image, timestamp, frame)
        # Recognize gestures
        recognize_gestures(gestures_recognizer, mp_image, timestamp, frame)

        fliped_frame = cv.flip(frame, 1)
        # Display the frame with hand landmarks and recognized gestures
        cv.imshow("WAVE Hand Tracking and Gesture Recognition", fliped_frame)
        if cv.waitKey(1) & 0xFF == ord("q"):
            break

        timestamp += int(1000 / cap.get(cv.CAP_PROP_FPS))

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
