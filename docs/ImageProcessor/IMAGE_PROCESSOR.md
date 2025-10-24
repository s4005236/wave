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
