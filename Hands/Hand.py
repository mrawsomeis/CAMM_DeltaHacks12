import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

THIS_DIR = Path(__file__).resolve().parent
MODEL_PATH = (THIS_DIR / "hand_landmarker.task").resolve()
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Hand model not found at: {MODEL_PATH}")

class HandMovementDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.positions = deque(maxlen=30)

    def detect_center(self, frame_bgr):
        # mediapipe Image expects SRGB data; convert BGR->RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = self.detector.detect(mp_image)

        if not result.hand_landmarks:
            return None

        h, w = frame_bgr.shape[:2]
        pts = [(int(l.x * w), int(l.y * h)) for l in result.hand_landmarks[0]]
        cx = int(np.mean([p[0] for p in pts]))
        cy = int(np.mean([p[1] for p in pts]))
        return (cx, cy)

    def close(self):
        self.detector.close()

def hand_moved(
    seconds: float = 3.0,
    camera_index: int = 0,
    pixel_delta_threshold: float = 18.0,
    min_detections: int = 3,
) -> bool:
    """
    Returns True if the hand center moves by >= pixel_delta_threshold
    (after at least min_detections detections) within `seconds`.
    """
    cap = cv2.VideoCapture(camera_index)
    detector = HandMovementDetector()

    start = time.time()
    detections = 0
    prev_center = None

    try:
        while time.time() - start < seconds:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            center = detector.detect_center(frame)
            if center is None:
                continue

            detections += 1

            if prev_center is not None:
                dx = center[0] - prev_center[0]
                dy = center[1] - prev_center[1]
                delta = (dx * dx + dy * dy) ** 0.5

                if detections >= min_detections and delta >= pixel_delta_threshold:
                    return True

            prev_center = center

        return False

    finally:
        cap.release()
        cv2.destroyAllWindows()
        detector.close()
