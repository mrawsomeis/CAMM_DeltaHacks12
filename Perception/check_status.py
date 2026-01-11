import time
import threading
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np
import os
import pickle

# ----------------------------
# Face setup (LBPH optional)
# ----------------------------
def _load_face_components(face_dir: str):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    recognizer = None
    id_to_name = {}

    model_path = os.path.join(face_dir, "trained_model.yml")
    pkl_path = os.path.join(face_dir, "id_to_name.pkl")

    # recognizer requires opencv-contrib-python
    if os.path.exists(model_path):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_path)

    if os.path.exists(pkl_path):
        with open(pkl_path, "rb") as f:
            id_to_name = pickle.load(f)

    return face_cascade, recognizer, id_to_name


# ----------------------------
# Hand setup (MediaPipe Tasks)
# ----------------------------
import mediapipe as mp
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

THIS_DIR = Path(__file__).resolve().parent
HAND_MODEL_PATH = (THIS_DIR / "hand_landmarker.task").resolve()
if not HAND_MODEL_PATH.exists():
    raise FileNotFoundError(f"Hand model not found at: {HAND_MODEL_PATH}")

class HandDetector:
    def __init__(self):
        base = python.BaseOptions(model_asset_path=str(HAND_MODEL_PATH))
        options = vision.HandLandmarkerOptions(
            base_options=base,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def hand_present(self, frame_bgr: np.ndarray) -> bool:
        # MP expects SRGB => give it RGB data
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        res = self.detector.detect(mp_image)
        return bool(res.hand_landmarks)

    def close(self):
        self.detector.close()


@dataclass
class PresenceResult:
    saw_hand: bool
    saw_face: bool
    face_id: Optional[str] = None  # known ID if recognized (else None)

    @property
    def status(self) -> str:
        if self.saw_hand and self.saw_face:
            return "both"
        if self.saw_hand:
            return "hand_only"
        if self.saw_face:
            return "face_only"
        return "neither"


def check_hand_and_face(
    seconds: float = 3.0,
    camera_index: int = 0,

    # face options
    face_dir: str = ".",                  # folder with trained_model.yml + id_to_name.pkl
    require_recognized_face: bool = False, # if True: only count face if model recognizes it
    face_confidence_threshold: float = 50.0,  # LBPH: lower = stricter

    # performance
    hand_fps_limit: float = 8.0,
    face_fps_limit: float = 10.0,

    show_window: bool = False,
) -> PresenceResult:
    """
    Runs for `seconds`, using ONE camera stream, and reports whether it saw:
      - a hand (MediaPipe)
      - a face (haar cascade; optionally recognized by LBPH)
    Returns summary at the end: hand/face/neither/both.
    """

    lock = threading.Lock()
    latest_frame: Optional[np.ndarray] = None
    stop = threading.Event()

    saw_hand = False
    saw_face = False
    face_id: Optional[str] = None

    face_cascade, recognizer, id_to_name = _load_face_components(face_dir)
    hand = HandDetector()

    # ------------ Camera producer ------------
    def camera_loop():
        nonlocal latest_frame
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            stop.set()
            return
        try:
            while not stop.is_set():
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                with lock:
                    latest_frame = frame

                if show_window:
                    cv2.imshow("Presence Check", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        stop.set()
                        break
        finally:
            cap.release()
            if show_window:
                cv2.destroyAllWindows()

    # ------------ Hand worker ------------
    def hand_loop():
        nonlocal saw_hand
        min_dt = 1.0 / max(1e-6, hand_fps_limit)
        last = 0.0
        while not stop.is_set():
            now = time.time()
            if now - last < min_dt:
                time.sleep(0.005)
                continue
            last = now

            with lock:
                frame = None if latest_frame is None else latest_frame.copy()
            if frame is None:
                continue

            try:
                if hand.hand_present(frame):
                    saw_hand = True
            except Exception:
                pass

    # ------------ Face worker ------------
    def face_loop():
        nonlocal saw_face, face_id
        min_dt = 1.0 / max(1e-6, face_fps_limit)
        last = 0.0
        while not stop.is_set():
            now = time.time()
            if now - last < min_dt:
                time.sleep(0.005)
                continue
            last = now

            with lock:
                frame = None if latest_frame is None else latest_frame.copy()
            if frame is None:
                continue

            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) == 0:
                    continue

                # Face is present
                if recognizer is None:
                    if not require_recognized_face:
                        saw_face = True
                    continue

                # Try recognizing first face
                x, y, w, h = faces[0]
                roi = gray[y:y+h, x:x+w]
                roi = cv2.resize(roi, (200, 200))
                pid, conf = recognizer.predict(roi)

                if conf < face_confidence_threshold:
                    saw_face = True
                    face_id = id_to_name.get(pid)
                else:
                    if not require_recognized_face:
                        saw_face = True

            except Exception:
                pass

    # Start threads
    t_cam = threading.Thread(target=camera_loop, daemon=True)
    t_hand = threading.Thread(target=hand_loop, daemon=True)
    t_face = threading.Thread(target=face_loop, daemon=True)

    t_cam.start()
    t_hand.start()
    t_face.start()

    # Run fixed window
    start = time.time()
    while time.time() - start < seconds:
        time.sleep(0.02)

    stop.set()

    # Cleanup
    try:
        hand.close()
    except Exception:
        pass

    return PresenceResult(saw_hand=saw_hand, saw_face=saw_face, face_id=face_id)
