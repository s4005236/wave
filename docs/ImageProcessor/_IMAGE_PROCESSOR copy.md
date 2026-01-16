# Recommended Version Combination for OpenCV + MediaPipe + Picamera2 on Raspberry Pi OS (Bookworm)

### Why These Versions Are Recommended

This configuration balances performance, compatibility, and stability on Raspberry Pi OS (Bookworm). It matches the exact versions from your `pyproject.toml` for your gesture recognition application.

---

### Operating System: Raspberry Pi OS (Bookworm)

- Bundled with **Python 3.11.2**, providing a consistent runtime for libraries such as OpenCV and MediaPipe.  
- Relies entirely on **`libcamera`**, the modern camera API replacing deprecated tools (`raspistill` / `bcm2835-v4l2`).  
- Out of the box, **Picamera2** integrates with `libcamera`, making it ideal for camera capture and frame streaming on Bookworm.

---

### Python >=3.11,<3.12

- Required for current **OpenCV** and **MediaPipe** ARM builds.  
- Matches the system Python packaged with Bookworm for both development consistency and dependency compatibility.  

---

### opencv-python <4.10

- Ensures compatibility with Raspberry Pi OS (Bookworm) and **libcamera**.  
- Avoids CMake and backend changes in versions ≥ 4.10 that disrupt Pi-specific integration.  
- Works seamlessly with **Python 3.11**, **numpy <2**, and Picamera2 frame pipelines.  

---

### numpy <2

- Provides compatibility with OpenCV <4.10 and MediaPipe 0.10.18 builds compiled against the pre-2.0 API.  
- Avoids ABI/API breaks introduced in numpy 2.0 that could cause import or segmentation faults.  

---

### mediapipe 0.10.18

- Complete framework for hand detection and landmarks computation directly from RGB input frames.  
- Leverages TensorFlow Lite under the hood but removes the need for explicit model handling.  
- Supported for ARMv7 and aarch64 with Python 3.11 via prebuilt wheels.  

---

### tflite-runtime ^2.14.0 (ARM only)

- Available only for `platform_machine == 'armv7l' or platform_machine == 'aarch64'`.  
- Provides stable TensorFlow Lite inference for MediaPipe models on Raspberry Pi.  

---

### picamera2 ^0.3.31 (ARM only)

- Available only for `platform_machine == 'armv7l' or platform_machine == 'aarch64'`.  
- Integrates with `libcamera` for camera capture on Raspberry Pi OS Bookworm.  

---

### Summary of Tested Working Versions (from pyproject.toml)

| Component | Version Constraint | Notes |
|------------|--------------------|-------|
| **OS** | Raspberry Pi OS (Bookworm) | Uses `libcamera`, includes Python 3.11 |
| **Python** | `>=3.11,<3.12` | System version compatibility |
| **OpenCV** | `<4.10` | Stable with Picamera2 and `libcamera` |
| **numpy** | `<2` | Compatible with OpenCV + MediaPipe |
| **mediapipe** | `0.10.18` | Integrated hand tracking + gesture inference |
| **picamera2** | `^0.3.31` | ARM only (`armv7l` / `aarch64`) |
| **tflite-runtime** | `^2.14.0` | ARM only (`armv7l` / `aarch64`) |

---

### Setup Instructions

1. **Install from your pyproject.toml:**

   ```bash
   pip install -e .[dev]
   ```

2. **Or create a virtual environment with system packages:**

   ```bash
   python3 -m venv .venv --system-site-packages
   source .venv/bin/activate
   pip install -e .
   ```

3. It's recommended to create this environment inside `/wave/wave/image` when developing or deploying the image processor module.

---

### Overview: Gesture Recognition Pipeline

Your application captures frames from the Raspberry Pi Camera, processes them using **OpenCV** and **MediaPipe**, classifies gestures based on hand landmarks, and visualizes results in real time.  

The processing flow:

1. **Video Capture:** Picamera2 provides RGB frames via the `libcamera` backend.  
2. **Landmark Detection:** MediaPipe Hands identifies hand pose landmarks in each frame.  
3. **Gesture Classification:** A Python logic layer determines specific gestures (thumbs up, fist, peace sign, etc.) from landmark geometry.  
4. **Visualization:** OpenCV overlays both the detected landmarks and gesture label onto the live video window.

---

### Functional Details

#### 1. Video Acquisition and Preprocessing

- The camera captures frames at a set resolution (e.g., 640×480).  
- Frames are flipped horizontally for a mirror effect.  
- Colors are converted from **BGR → RGB** to suit MediaPipe's expected input format.  

#### 2. Hand Landmark Detection

- MediaPipe Hands returns up to two sets of landmarks (each with 21 points).  
- These landmarks represent anatomical positions such as wrist, finger tips, and joints.

#### 3. Gesture Classification Logic

Each frame's hand landmarks are passed into the `classify_gesture()` function, which decides the current gesture by analyzing relative joint positions:

- **THUMBS_UP / THUMBS_DOWN:** Determined by the thumb's relative position to the wrist and joint alignment.  
- **PEACE_SIGN:** Index and middle fingers extended; ring and pinky curled.  
- **OPEN_HAND:** All fingers extended.  
- **FIST:** All fingers curled; thumb folded.  
- **POINT_UP / POINT_DOWN:** Only index finger extended, pointing relative to wrist height.  
- **UNKNOWN:** All other combinations.

#### 4. Rendering

- Gesture names and hand landmarks are drawn directly on the video stream with OpenCV's `putText()` and `draw_landmarks()`.  
- Press **"q"** to exit the live feed gracefully.

---

### Example Execution

Run the program with:

```bash
python3 gesture_recognition.py
```

Once the camera starts, the terminal will log:

```
Camera started. Press 'q' to quit.
```

The display window will show your live video with detected landmarks and recognized gestures.