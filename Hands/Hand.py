import cv2
import mediapipe as mp
import numpy as np
import os
import time
from collections import deque

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

testing = False
seconds = 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, "hand_landmarker.task")

class HandMovementDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = vision.HandLandmarker.create_from_options(options)
        self.positions = deque(maxlen=30)
        self.movement_threshold = 8

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = self.detector.detect(mp_image)

        if not result.hand_landmarks:
            return None, None

        h, w, _ = frame.shape
        pts = [(int(l.x * w), int(l.y * h)) for l in result.hand_landmarks[0]]

        cx = int(np.mean([p[0] for p in pts]))
        cy = int(np.mean([p[1] for p in pts]))
        return pts, (cx, cy)

    def calculate_movement(self, center):
        if not center:
            return 0

        self.positions.append(center)
        if len(self.positions) < 2:
            return 0

        dist = 0
        for i in range(1, len(self.positions)):
            dx = self.positions[i][0] - self.positions[i-1][0]
            dy = self.positions[i][1] - self.positions[i-1][1]
            dist += (dx*dx + dy*dy)**0.5

        return dist / len(self.positions)

    def direction(self):
        if len(self.positions) < 10:
            return "N/A"

        sx, sy = self.positions[0]
        ex, ey = self.positions[-1]
        dx, dy = ex - sx, ey - sy

        if abs(dx) < 15 and abs(dy) < 15:
            return "STATIONARY"

        return "RIGHT" if abs(dx) > abs(dy) and dx > 0 else \
               "LEFT" if abs(dx) > abs(dy) else \
               "DOWN" if dy > 0 else "UP"

    def draw(self, frame, pts, center, movement):
        if pts:
            for p in pts:
                cv2.circle(frame, p, 4, (0, 255, 255), -1)

        if center:
            cv2.circle(frame, center, 6, (0, 0, 255), -1)

        if len(self.positions) > 1:
            cv2.polylines(frame, [np.array(self.positions)], False, (255, 200, 0), 2)

        status = "MOVING" if movement > self.movement_threshold else "STATIONARY"
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0,255,0) if status=="STATIONARY" else (0,0,255), 2)
        cv2.putText(frame, f"{movement:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255,255,255), 2)
        cv2.putText(frame, self.direction(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255,255,255), 2)


def hand_moved(seconds=2.0, pixel_delta_threshold=18, min_detections=3, camera_index=0):
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

            _, center = detector.detect(frame)
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

if testing:
    cap = cv2.VideoCapture(0)
    detector = HandMovementDetector()

    while 1:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        pts, center = detector.detect(frame)
        movement = detector.calculate_movement(center)
        detector.draw(frame, pts, center, movement)

        cv2.imshow("Hand Movement Skeleton", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

moved = hand_moved(seconds)
print(moved)
