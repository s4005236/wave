import math
from enum import Enum

import cv2
import mediapipe as mp
import numpy as np
from picamera2 import Picamera2

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class Gesture(Enum):
    THUMBS_UP = "THUMBS_UP"
    OPEN_HAND = "OPEN_HAND"
    PEACE_SIGN = "PEACE_SIGN"
    FIST = "FIST"
    POINT_UP = "POINT_UP"
    POINT_DOWN = "POINT_DOWN"
    UNKNOWN = "UNKNOWN"


# Landmark indices for convenience
THUMB_TIP = 4
THUMB_IP = 3
THUMB_MCP = 2
INDEX_MCP = 5
INDEX_PIP = 6
INDEX_DIP = 7
INDEX_TIP = 8
MIDDLE_PIP = 10
MIDDLE_TIP = 12
RING_PIP = 14
RING_TIP = 16
PINKY_PIP = 18
PINKY_TIP = 20
WRIST = 0


def _is_finger_extended_y(tip, pip, direction="up"):
    """
    direction='up'  : tip above PIP  (smaller y)
    direction='down': tip below PIP  (larger y)
    """
    if direction == "up":
        return tip.y < pip.y
    else:
        return tip.y > pip.y


def _is_thumb_up(hand_landmarks):
    wrist = hand_landmarks.landmark[WRIST]
    thumb_tip = hand_landmarks.landmark[THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[THUMB_MCP]

    # Thumb extended if tip is far from MCP and roughly aligned vertically
    extended = (
        abs(thumb_tip.x - thumb_mcp.x) < 0.15
        and thumb_tip.y < thumb_ip.y < thumb_mcp.y
    )
    # Above wrist for "thumbs up"
    above_wrist = thumb_tip.y < wrist.y
    return extended and above_wrist


def _is_thumb_down(hand_landmarks):
    wrist = hand_landmarks.landmark[WRIST]
    thumb_tip = hand_landmarks.landmark[THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[THUMB_MCP]

    extended = (
        abs(thumb_tip.x - thumb_mcp.x) < 0.15
        and thumb_tip.y > thumb_ip.y > thumb_mcp.y
    )
    below_wrist = thumb_tip.y > wrist.y
    return extended and below_wrist


def _finger_states(hand_landmarks):
    lms = hand_landmarks.landmark

    index_extended = _is_finger_extended_y(
        lms[INDEX_TIP], lms[INDEX_PIP], "up"
    )
    middle_extended = _is_finger_extended_y(
        lms[MIDDLE_TIP], lms[MIDDLE_PIP], "up"
    )
    ring_extended = _is_finger_extended_y(lms[RING_TIP], lms[RING_PIP], "up")
    pinky_extended = _is_finger_extended_y(
        lms[PINKY_TIP], lms[PINKY_PIP], "up"
    )

    return {
        "index": index_extended,
        "middle": middle_extended,
        "ring": ring_extended,
        "pinky": pinky_extended,
    }


def classify_gesture(hand_landmarks) -> str:
    lms = hand_landmarks.landmark
    states = _finger_states(hand_landmarks)

    index_up = states["index"]
    middle_up = states["middle"]
    ring_up = states["ring"]
    pinky_up = states["pinky"]

    thumb_up = _is_thumb_up(hand_landmarks)
    thumb_down = _is_thumb_down(hand_landmarks)

    if (
        thumb_up
        and not index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):
        return "THUMBS_UP"

    if index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE_SIGN"

    if thumb_up and index_up and middle_up and ring_up and pinky_up:
        return "OPEN_HAND"

    if (
        not index_up
        and not middle_up
        and not ring_up
        and not pinky_up
        and not thumb_up
        and not thumb_down
    ):
        return "FIST"

    wrist = lms[WRIST]
    index_tip = lms[INDEX_TIP]

    if (
        index_up
        and not middle_up
        and not ring_up
        and not pinky_up
        and index_tip.y < wrist.y
    ):
        return "POINT_UP"

    if (
        not middle_up
        and not ring_up
        and not pinky_up
        and index_tip.y > wrist.y
    ):
        return "POINT_DOWN"

    return "UNKNOWN"


def main():
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    picam2 = Picamera2()
    picam2.configure(
        picam2.create_video_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
    )
    picam2.start()

    print("Camera started. Press 'q' to quit.")

    while True:
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 1)

        """Get image width and heigh"""
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                print(hand_landmarks.landmark[0])
                gesture = classify_gesture(hand_landmarks)

                wrist_lm = hand_landmarks.landmark[0]
                cx, cy = int(wrist_lm.x * w), int(wrist_lm.y * h)
                cv2.putText(
                    frame,
                    gesture,
                    (cx - 40, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        cv2.imshow("MediaPipe Gestures", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
