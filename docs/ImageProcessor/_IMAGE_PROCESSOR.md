# Recommended Version Combination for OpenCV + TensorFlow Lite on Raspberry Pi OS (Bookworm)

### Why are these Versions Recommended?

---

### Operating System: PiOS (Bookworm)
- Comes with **Python 3.11.2 preinstalled**, making setup simpler and more consistent.  
- Uses **`libcamera`** instead of the deprecated `raspistill` / `bcm2835-v4l2` stack.  
- Ensures camera access through `libcamera`, which is supported by OpenCV 4.9.  

---

### Python 3.11
- Essential because older **OpenCV** and **TensorFlow Lite** ARM builds are **no longer compiled for Python < 3.11**.  
- Many **newer TensorFlow Lite versions** are **not yet fully compatible** with Python 3.11 or lack ARM builds.  
- Matches the Python version provided by Bookworm for maximum compatibility and stability.  

---

### OpenCV 4.9.0.80
- Last version that runs **stably on Raspberry Pi OS Bookworm** with the **`libcamera` stack**.  
- Versions ≥ 4.10 introduced **CMake and backend changes** causing conflicts with Pi-specific components like `libopencv-videoio`.  
- Works reliably with **Python 3.11** and **numpy 1.26.x**, avoiding camera initialization issues and import errors.  

---

### numpy 1.26.4
- **TensorFlow Lite 2.14** was compiled for **numpy < 2.0**.  
- **OpenCV 4.9** was also tested and built for the 1.26.x API.  
- Prevents breaking changes introduced in **numpy 2.0** (which changes parts of the C-API), avoiding import or segmentation errors.  

---

### tflite_runtime 2.14.0
- Last **officially built version for ARM (Raspberry Pi)** that remains **compatible with Python 3.11**.  
- Later versions (2.15+, 2.16+) often require **numpy ≥ 2.0** and are **not consistently available for ARM architectures**.  
- Provides stable inference performance with **TensorFlow Lite models** on Raspberry Pi OS Bookworm.  

---

### Summary of Known Working Versions

| Component | Version | Notes |
|------------|----------|-------|
| **OS** | Raspberry Pi OS (Bookworm) | Uses `libcamera`, Python 3.11 preinstalled |
| **Python** | 3.11.2 | Required for TFLite 2.14 compatibility |
| **OpenCV** | 4.9.0.80 | Last stable version supporting `libcamera` and numpy 1.26 |
| **numpy** | 1.26.4 | Last pre-2.0 API; compatible with both OpenCV & TFLite |
| **tflite_runtime** | 2.14.0 | Last ARM build working with Python 3.11 |

---

### Setup

- when developing or running the code in a virtual environment, enable --system-site-packages when creating a venv
- This step is important because picamera2 requires access to `libcamera` in order to use the Raspberry Pi Camera Module
```python3 -m venv .venv --system-site-packages```
- note: It's recommended to create the virtual environment in the `/wave/wave/image` directory when working with the code of the image processor module.


### Overview: Use of OpenCV and TensorFlow Lite

- OpenCV serves as the primary framework for capturing and manipulating the video stream.
- TensorFlow Lite provides the runtime environment for executing lightweight machine learning models.
- Machine learning models are employed to perform hand-gesture recognition.
- One model is responsible for detecting the presence and location of a hand.
- A second model computes 21 anatomical landmark points on the detected hand.

### Details

#### OpenCV for Video Acquisition and Preprocessing
- OpenCV initializes and manages the video stream at the specified resolution.
- It is used to resize frames to match the input requirements of the machine learning models.
- Each frame is captured and converted into the appropriate color format or channel configuration, as different ML models may require different input types.

#### Color Space and Channel Handling
- The Raspberry Pi Picamera delivers frames in BGRA format by default.
- Most object and hand-detection models are trained on RGB images, making a conversion from BGRA to RGB necessary.
- If a model expects grayscale input, the color channels must be reduced accordingly.
- Grayscale processing can improve computational efficiency on resource-constrained devices such as the Raspberry Pi.

#### Data Type Conversion and Normalization
- Prior to inference, the frame data must be normalized to meet the expectations of the TensorFlow Lite model.
- TFLite models typically accept:
  - `uint8` pixel values in the range 0–255, or
  - `float32` pixel values normalized to the range 0–1.
- The frame is resized, normalized, and supplied to the palm detection model (`palm_detection_without_custom_layer.tflite`) as input.

#### Palm Detection Model
- The palm detection model returns a bounding box that identifies the location of the hand within the frame.

#### Hand Landmark Model
- The bounding box coordinates are used to extract and crop the relevant hand region from the frame.
- The cropped image is resized to 224×224 pixels to meet the model's input specifications.
- This processed image is passed to the hand landmark model (`hand_landmark_lite.tflite`), which outputs 21 landmark points representing key positions on the hand.
- These landmarks can then be used to implement gesture-recognition logic in Python.

#### Rendering the Processed Output
- After inference and processing, the resulting video frame is displayed using OpenCV's window and rendering functions.
