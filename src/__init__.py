#!/usr/bin/env python3
"""
hand_gesture_server.py

Erläuterung (kurz):
- Öffnet die PiCam (OpenCV VideoCapture) in 640x480.
- Wandelt jeden Frame in Graustufen um und dupliziert die Kanalwerte (TFLite-Modelle
  erwarten meist 3 Kanäle).
- Verwendet BlazePalm (.tflite) für eine Hand-Bounding-Box (palm_detection_without_custom_layer.tflite).
- Cropt die Handregion und verwendet hand_landmark_lite.tflite für 21 Landmarken.
- Klassifiziert mit einer einfachen Regel "Daumen über/unter Handgelenk" -> thumbs_up / thumbs_down / none.
- Stellt eine kleine HTTP-API bereit (GET /gesture), die den aktuellen Gestenzustand als JSON liefert.
- Visualisiert das Ergebnis per OpenCV-Fenster (Landmarks + BoundingBox + Text).

Achte darauf, dass die Modelle in:
    ./models/palm_detection_without_custom_layer.tflite
    ./models/hand_landmark_lite.tflite
liegen (Dateinamen exakt wie hier angegeben).
"""

import cv2
import numpy as np
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import sys
import os

# Versuch, die leichtgewichtige TFLite-Runtime zu importieren (empfohlen für Raspberry Pi).
# Falls sie nicht installiert ist, verwenden wir als Fallback das volle TensorFlow (oft nicht auf Raspi).
try:
    import tflite_runtime.interpreter as tflite
except Exception:
    import tensorflow as tf
    tflite = tf.lite

# -------------------------
# Konfiguration
# -------------------------
PALM_MODEL_PATH = "models/palm_detection_without_custom_layer.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark_lite.tflite"

CAM_ID = 0             # Index der Kamera (0 ist Standard)
CAM_WIDTH = 640        # Breite (px)
CAM_HEIGHT = 480       # Höhe (px)

API_HOST = "0.0.0.0"   # Bind an alle Interfaces (lokales Netzwerk)
API_PORT = 8080        # Port für die HTTP-API

# globaler Gestenzustand (wird von Kamera-Thread gesetzt und von API gelesen)
current_gesture = "none"
gesture_lock = threading.Lock()
last_seen = 0.0  # Unix-Timestamp, wann eine nicht-"none"-Geste zuletzt erkannt wurde

# -------------------------
# Hilfsfunktion: Interpreter laden
# -------------------------
def make_interpreter(model_path):
    """
    Lädt ein TFLite-Modell und initialisiert den Interpreter.
    Wir werfen einen Fehler, falls die Datei nicht existiert.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

print("Lade Modelle...")
palm_interpreter = make_interpreter(PALM_MODEL_PATH)
palm_input_details = palm_interpreter.get_input_details()
palm_output_details = palm_interpreter.get_output_details()

landmark_interpreter = make_interpreter(LANDMARK_MODEL_PATH)
landmark_input_details = landmark_interpreter.get_input_details()
landmark_output_details = landmark_interpreter.get_output_details()
print("Modelle geladen.")

# Debug-Ausgabe der Input-Details (nützlich beim Abstimmen / Debuggen)
print("Palm input:", palm_input_details)
print("Landmark input:", landmark_input_details)

# -------------------------
# Preprocessing: Bild passend machen für das Modell
# -------------------------
def preprocess_for_interpreter(img, input_details):
    """
    Bereitet ein Bild so vor, dass es in den TFLite-Interpreter passt.

    img: H x W x 3 uint8 (z.B. Graustufen gestapelt als 3 Kanäle)
    input_details: interpreter.get_input_details()[0]

    Rückgabe: np.array mit Shape (1, H_model, W_model, C) und korrektem dtype / quantisierung
    """
    expected_dtype = input_details['dtype']          # z.B. np.uint8 oder np.float32
    shape = input_details['shape']                   # typischerweise (1, H, W, C)
    h, w = shape[1], shape[2]

    # Auf Modellauflösung skalieren (interne Modelle erwarten z.B. 128x128 / 192x192)
    resized = cv2.resize(img, (w, h))

    if expected_dtype == np.float32:
        # Float-Modelle erwarten Werte 0..1
        input_data = resized.astype(np.float32) / 255.0
        input_data = np.expand_dims(input_data, axis=0)
    else:
        # Quantisierte Modelle (meist uint8 oder int8) benötigen scale / zero_point
        input_data = resized.astype(np.uint8)
        # Quantisierungsparameter (scale, zero_point) können im input_details enthalten sein
        scale, zero_point = 1.0, 0
        if 'quantization' in input_details and input_details['quantization']:
            scale, zero_point = input_details['quantization']

        if expected_dtype == np.uint8:
            # Wenn scale vorhanden, wende quantisierung an: q = round(input/scale) + zero_point
            if scale != 0 and scale != 1.0:
                q = np.clip((input_data / scale + zero_point).round(), 0, 255).astype(np.uint8)
            else:
                q = input_data
            input_data = np.expand_dims(q, axis=0)
        elif expected_dtype == np.int8:
            if scale != 0 and scale != 1.0:
                q = np.clip((input_data / scale + zero_point).round(), -128, 127).astype(np.int8)
            else:
                q = input_data.astype(np.int8)
            input_data = np.expand_dims(q, axis=0)
        else:
            # Fallback: cast auf erwarteten dtype
            input_data = np.expand_dims(input_data.astype(expected_dtype), axis=0)

    return input_data

# -------------------------
# BlazePalm Detection: Bounding Box der Hand finden
# -------------------------
def detect_palm_bbox(frame_bgr):
    """
    Übergibt das gegebene Frame (HxWx3 BGR) an das Palm-Modell
    und gibt eine Bounding-Box im Originalbild-Koordinatensystem zurück.

    Rückgabe: (xmin, ymin, xmax, ymax) oder None, falls keine Hand gefunden.
    """
    try:
        # frame_bgr sollte bereits das "3-kanal" Bild sein (z.B. Graustufen gestapelt)
        input_data = preprocess_for_interpreter(frame_bgr, palm_input_details)
        palm_interpreter.set_tensor(palm_input_details[0]['index'], input_data)
        palm_interpreter.invoke()

        # Die Ausgaben können variieren; wir lesen alle Outputs und versuchen heuristisch Boxes/Scores zu finden
        outs = [palm_interpreter.get_tensor(o['index']) for o in palm_output_details]

        boxes = None
        scores = None
        # Heuristiken: Tensor mit letzter Dim == 4 -> Boxen, 1D/Tensor mit Scores -> scores
        for out in outs:
            if out.ndim >= 2 and out.shape[-1] == 4:
                boxes = out
            elif out.ndim >= 1 and (out.shape[-1] == 1 or out.ndim == 1):
                scores = out.squeeze()

        # Falls heuristik nichts findet, fallback auf die ersten beiden outputs
        if boxes is None or scores is None:
            if len(outs) >= 2:
                boxes = outs[0]
                scores = outs[1].squeeze()
            else:
                return None

        b = np.array(boxes).squeeze()
        s = np.array(scores).squeeze()

        # Wenn mehrere Boxen vorhanden: wähle die mit höchstem Score
        if b.ndim == 1:
            box = b
            score = float(s) if np.isscalar(s) else float(s[0])
        else:
            if s.ndim == 0:
                score = float(s)
                box = b[0]
            else:
                idx = int(np.argmax(s))
                score = float(s[idx])
                box = b[idx]

        # Confidence-Filter: erfordert mindestens mittlere Sicherheit
        if score < 0.5:
            return None

        # Box wird oft im Normalized-Format [ymin, xmin, ymax, xmax] geliefert
        h, w, _ = frame_bgr.shape
        ymin, xmin, ymax, xmax = box[0], box[1], box[2], box[3]

        # In Pixel umrechnen
        xmin_i = max(0, int(xmin * w))
        ymin_i = max(0, int(ymin * h))
        xmax_i = min(w, int(xmax * w))
        ymax_i = min(h, int(ymax * h))

        # Einen kleinen Padding-Bereich hinzufügen, damit die ganze Hand im Crop ist
        pad_x = int(0.15 * (xmax_i - xmin_i))
        pad_y = int(0.15 * (ymax_i - ymin_i))
        xmin_i = max(0, xmin_i - pad_x)
        ymin_i = max(0, ymin_i - pad_y)
        xmax_i = min(w, xmax_i + pad_x)
        ymax_i = min(h, ymax_i + pad_y)

        # Wenn die Box zu klein ist, verwirf sie
        if xmax_i - xmin_i <= 10 or ymax_i - ymin_i <= 10:
            return None

        return (xmin_i, ymin_i, xmax_i, ymax_i)
    except Exception:
        # Bei Fehlern in der Inferenz geben wir None zurück (robustheit)
        return None

# -------------------------
# Hand-Landmark Inferenz
# -------------------------
def detect_landmarks(cropped_bgr):
    """
    Führt das Landmark-Modell auf dem Hand-Crop aus.
    Erwartet: cropped_bgr HxWx3 BGR (z.B. Graustufen gestapelt)
    Rückgabe: numpy array (21,3) mit Normalisierten [x,y,z] Werten (oder None bei Fehler)
    """
    try:
        input_data = preprocess_for_interpreter(cropped_bgr, landmark_input_details)
        landmark_interpreter.set_tensor(landmark_input_details[0]['index'], input_data)
        landmark_interpreter.invoke()

        out = landmark_interpreter.get_tensor(landmark_output_details[0]['index'])
        out = np.array(out).squeeze()
        # Häufig liefert das Modell (1,63) -> reshape zu (21,3)
        if out.size == 63:
            lm = out.reshape((21, 3))
        elif out.ndim == 2 and out.shape[1] == 3:
            lm = out
        else:
            lm = out.reshape((21, 3))
        return lm
    except Exception:
        return None

# -------------------------
# Klassifikator: Daumen hoch / runter
# -------------------------
def classify_thumb_gesture(landmarks):
    """
    Sehr einfache Regel-basierte Klassifikation:
    - Verwende y-Koordinaten (in normalisierter Crop-Koordinate; y größer -> weiter unten im Bild)
    - Wrist index = 0, Thumb tip index = 4 (MediaPipe-Konvention)
    - Wenn Daumen-Spitze deutlich oberhalb des Handgelenks -> thumbs_up
    - Wenn deutlich unterhalb -> thumbs_down
    - Sonst -> none

    Hinweis: Threshold anpassbar (TH)
    """
    if landmarks is None or landmarks.shape[0] < 5:
        return "none"

    wrist_y = float(landmarks[0][1])
    thumb_tip_y = float(landmarks[4][1])

    TH = 0.12  # wie "weit" die Daumen-Spitze relativ zum Handgelenk liegen muss

    if thumb_tip_y < wrist_y - TH:
        return "thumbs_up"
    if thumb_tip_y > wrist_y + TH:
        return "thumbs_down"
    return "none"

# -------------------------
# HTTP API: /gesture Endpoint
# -------------------------
class GestureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Nur einen Endpunkt anbieten: /gesture
        if self.path == "/gesture":
            with gesture_lock:
                g = current_gesture
                last = last_seen
            resp = {"gesture": g, "last_seen": last}
            body = json.dumps(resp).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            # Alle anderen Routen -> 404
            self.send_response(404)
            self.end_headers()

def run_server():
    """
    Startet einen simplen HTTP-Server im aktuellen Thread (in der Praxis
    starten wir ihn in einem separaten Daemon-Thread).
    """
    server = HTTPServer((API_HOST, API_PORT), GestureHandler)
    print(f"API Server läuft auf http://{API_HOST}:{API_PORT}/gesture")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

# -------------------------
# Kamera-Hauptschleife
# -------------------------
def run_camera_loop():
    """
    Hauptschleife: liest Frames, preprocess, erkennt Hand, Landmark, klassifiziert,
    visualisiert das Ergebnis und aktualisiert den globalen Gestenzustand.
    """
    global current_gesture, last_seen

    # Versuch, V4L2-Backend zu benutzen (stabiler mit PiCam/libcamera)
    cap = cv2.VideoCapture(CAM_ID, cv2.CAP_V4L2)
    if not cap.isOpened():
        # Fallback: ohne expliziten Backend-Parameter
        cap = cv2.VideoCapture(CAM_ID)

    # Setze die gewünschte Auflösung
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)

    if not cap.isOpened():
        print("Fehler: Kamera nicht geöffnet. Prüfe Picam / VideoCapture ID.")
        return

    print("Starte Kamera (640x480). Drücke 'q' im Fenster zum Beenden.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # Falls Kamera kurzzeitig keinen Frame liefert: kurz warten und weiter
                time.sleep(0.01)
                continue

            # 1) Graustufen erzeugen (reduziert Datenmenge / verrauschte Farbinformation)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 2) Model erwartet 3 Kanäle -> Graustufen dreifach zusammenführen
            #    Dadurch behalten wir CPU-Vorteile von Graustufen, liefern aber 3-kanal input.
            stacked = cv2.merge([gray, gray, gray])  # H x W x 3, dtype uint8

            # 3) Palm-Detection: Bounding Box für Hand (oder None)
            bbox = detect_palm_bbox(stacked)
            gesture = "none"

            if bbox:
                xmin, ymin, xmax, ymax = bbox
                crop = stacked[ymin:ymax, xmin:xmax]  # Crop in 3-Kanal-Format
                if crop.size > 0:
                    # 4) Landmark-Inferenz auf dem Crop
                    lm = detect_landmarks(crop)
                    if lm is not None:
                        # 5) Klassifizieren
                        gesture = classify_thumb_gesture(lm)

                        # 6) Visualisierung: Landmarken zurück auf Fullframe mappen und zeichnen
                        for (x_rel, y_rel, z) in lm:
                            cx = int(xmin + x_rel * (xmax - xmin))
                            cy = int(ymin + y_rel * (ymax - ymin))
                            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

                # Bounding Box auf das Original-Frame zeichnen
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

            # Globalen Zustand threadsicher aktualisieren
            with gesture_lock:
                if gesture != current_gesture:
                    current_gesture = gesture
                if gesture != "none":
                    last_seen = time.time()

            # 7) GUI-Text
            display_text = f"Geste: {current_gesture}"
            cv2.putText(frame, display_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

            # 8) Fenster anzeigen
            cv2.imshow("Hand Gesture (press q to quit)", frame)

            # Beende bei 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        # Sauber beenden bei STRG+C
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()

# -------------------------
# Programmstart
# -------------------------
if __name__ == "__main__":
    # 1) HTTP-Server in einem separaten Daemon-Thread starten
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 2) Kamera-Hauptschleife (blockierend im Hauptthread)
    run_camera_loop()

    print("Beende...")
    sys.exit(0)

