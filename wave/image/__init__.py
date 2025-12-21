import math

import cv2
import mediapipe as mp
import numpy as np
from picamera2 import Picamera2

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


# Simple gesture classifier using landmark geometry
def classify_gesture(hand_landmarks, image_width, image_height):
    # Convert landmarks to pixel coords for convenience
    pts = []
    for lm in hand_landmarks.landmark:
        pts.append(np.array([lm.x * image_width, lm.y * image_height]))

    # Indices in MediaPipe Hands:
    # 0: wrist
    # Thumb: 1,2,3,4
    # Index: 5,6,7,8
    # Middle: 9,10,11,12
    # Ring: 13,14,15,16
    # Pinky: 17,18,19,20

    wrist = pts[0]
    thumb_tip = pts[4]
    index_tip = pts[8]
    middle_tip = pts[12]
    ring_tip = pts[16]
    pinky_tip = pts[20]

    # Distances from wrist to fingertips
    def dist(a, b):
        return np.linalg.norm(a - b)

    d_thumb = dist(wrist, thumb_tip)
    d_index = dist(wrist, index_tip)
    d_middle = dist(wrist, middle_tip)
    d_ring = dist(wrist, ring_tip)
    d_pinky = dist(wrist, pinky_tip)

    # Heuristic thresholds (tune as needed)
    avg_finger = (d_index + d_middle + d_ring + d_pinky) / 4.0

    # Fist: all fingers close to wrist
    if avg_finger < 80:
        return "FIST"

    # Open hand: all fingers far from wrist
    if avg_finger > 140:
        return "OPEN_HAND"

    # Thumbs up: thumb far, others closer, and thumb above wrist
    if d_thumb > 120 and avg_finger < 130 and thumb_tip[1] < wrist[1]:
        return "THUMBS_UP"

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

        # Get image width and height
        h, w, _ = frame.shape  # <--- ADD THIS LINE

        # If your frame is RGB already, skip conversion OR fix it as below:
        # If frame is actually RGB from Picamera2, do NOT convert BGR->RGB.
        # For safety on many setups, just do:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                print(hand_landmarks.landmark[0])
                gesture = classify_gesture(hand_landmarks, w, h)

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
