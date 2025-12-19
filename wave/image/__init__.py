import time

import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from picamera2 import Picamera2

FPS = 20
FRAME_TIME = 1.0 / FPS  # time between two frames

picam = (
    Picamera2()
)  # is needed to use Raspberry Pi Cameras that are connected via CSI Interface
picam.configure(
    picam.create_preview_configuration(main={"size": (640, 480)})
)  # heighth and width of the videostream
picam.start()
time.sleep(1)

# loads palm detection
palm_interpreter = tflite.Interpreter(
    model_path="src/image_processing/tflite_models/palm_detection_without_custom_layer.tflite"
)
palm_interpreter.allocate_tensors()
palm_input_details = palm_interpreter.get_input_details()
palm_output_details = palm_interpreter.get_output_details()

print("=== Palm Model Output Details ===")
for i, d in enumerate(palm_output_details):
    print(
        f"Output {i}: index={d['index']} shape={d['shape']} dtype={d['dtype']}"
    )
print("================================")


# loads hand landmark
landmark_interpreter = tflite.Interpreter(
    model_path="src/image_processing/tflite_models/hand_landmark_lite.tflite"
)
landmark_interpreter.allocate_tensors()
landmark_input_details = landmark_interpreter.get_input_details()
landmark_output_details = landmark_interpreter.get_output_details()

while True:
    start = time.time()

    # raw camera frame
    frame_raw = picam.capture_array()

    # frame for ML model (RGB)
    frame = cv2.cvtColor(frame_raw, cv2.COLOR_BGRA2RGB)

    # frame for OpenCV display (BGR)
    frame_bgr = cv2.cvtColor(frame_raw, cv2.COLOR_BGRA2BGR)

    # --- Palm Detection ---

    # Debug: show expected input details
    expected_shape = palm_input_details[0]["shape"]  # e.g. [1, 256, 256, 3]
    expected_dtype = palm_input_details[0]["dtype"]  # e.g. np.float32

    # expected_shape is a numpy array; convert to python ints
    b, h_exp, w_exp, c_exp = map(int, expected_shape)

    # Resize: cv2.resize expects (width, height)
    palm_img = cv2.resize(frame, (w_exp, h_exp))

    # Channels: model may expect 1 or 3 channels
    if c_exp == 1:
        # convert to grayscale (single channel)
        print("[WARN] Model expects 1 channel — converting to grayscale.")
        palm_img = cv2.cvtColor(palm_img, cv2.COLOR_RGB2GRAY)
        # make it H x W x 1
        palm_img = np.expand_dims(palm_img, axis=-1)
    elif c_exp == 3:
        # already in 3 channel RGB format
        pass
    else:
        raise ValueError(
            f"error: unexpected amount of channels in the model: {c_exp}"
        )

    # datatypes and normalization:
    # MediaPipe Palm Detection expects float32 in range [-1, +1]
    if expected_dtype == np.uint8:
        palm_input = np.expand_dims(palm_img.astype(np.uint8), axis=0)
    else:
        palm_input = np.expand_dims(
            (palm_img.astype(np.float32) / 127.5) - 1.0, axis=0
        )

    # output for debugging and troubleshooting
    print("Model expects shape:", expected_shape, "dtype:", expected_dtype)
    print(
        "Prepared input shape:", palm_input.shape, "dtype:", palm_input.dtype
    )

    # safety check before set_tensor
    if palm_input.shape != tuple(expected_shape.tolist()):
        raise ValueError(
            f"Input shape does not match model: prepared={palm_input.shape} expected={tuple(expected_shape.tolist())}"
        )

    # writes frame into model entry
    palm_interpreter.set_tensor(palm_input_details[0]["index"], palm_input)

    # start palm_detection to calculate output
    palm_interpreter.invoke()

    # read ALL palm outputs
    palm_outputs = []
    for d in palm_output_details:
        palm_outputs.append(palm_interpreter.get_tensor(d["index"]))

    # --- DEBUG: show palm score (confidence only, no box decoding yet) ---
    # Output 1 has shape [1, 2944, 1] -> confidence per anchor
    scores = palm_outputs[1]
    max_score = float(scores.max())

    cv2.putText(
        frame_bgr,
        f"Max palm score: {max_score:.3f}",
        (10, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        2,
    )

    # analyse palm_output -> bounding box of hand
    # e.g. palm_box = [x_min, y_min, x_max, y_max] (normalized to 0–1)
    # NOTE:
    # This model outputs 2944 anchors and requires anchor decoding.
    # Bounding box extraction will be implemented in the next step.

    # --- Crop & Resize for hand_landmark model ---
    # crop hand area using palm_box
    # hand_img = frame[y_min:y_max, x_min:x_max]
    # hand_img = cv2.resize(hand_img, (224,224))
    # landmark_input = np.expand_dims(hand_img.astype(np.float32)/255.0, axis=0)

    # landmark_interpreter.set_tensor(landmark_input_details[0]['index'], landmark_input)
    # landmark_interpreter.invoke()
    # landmark_output = landmark_interpreter.get_tensor(landmark_output_details[0]['index'])
    # landmark_output -> 21 hand landmarks

    cv2.imshow(
        "wave - Wenn du das hier siehst, hast du ein Bild ^^",
        frame_bgr,
    )

    if cv2.waitKey(1) & 0xFF == ord(
        "q"
    ):  # returns ASCII-Code of the given Key; 0xFF ensures that only the last 8 bits of the actual key are being used
        break

    elapsed = time.time() - start
    delay = max(
        0, FRAME_TIME - elapsed
    )  # ensures positive numbers in case the loop needs more time than the fps cap
    time.sleep(delay)  # "dynamic" delay based on the runtime of the loop

picam.close()
cv2.destroyAllWindows()
