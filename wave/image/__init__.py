import cv2
import mediapipe as mp
from picamera2 import Picamera2
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

print("Camera started. Press 'q' to quit.")

while True:
    # Capture frame from picamera2
    frame = picam2.capture_array()
    
    # Flip frame horizontally for mirror effect (optional)
    frame = cv2.flip(frame, 1)
    
    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Process with MediaPipe
    results = hands.process(rgb_frame)
    
    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display frame
    cv2.imshow('MediaPipe + Picamera2 + OpenCV', frame)
    
    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
picam2.stop()
cv2.destroyAllWindows()
