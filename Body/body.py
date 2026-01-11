import time
import math
import threading
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pathlib import Path

# ============================================================
# Resolve model path ABSOLUTELY (relative to this file)
# ============================================================
THIS_DIR = Path(__file__).resolve().parent
MODEL_PATH = (THIS_DIR / "pose_landmarker.task").resolve()

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Pose model not found at: {MODEL_PATH}")

# ============================================================
# Pose skeleton connections (BlazePose-style)
# ============================================================
POSE_CONNECTIONS = [
    # Torso
    (11, 12), (11, 23), (12, 24), (23, 24),

    # Left arm
    (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),

    # Right arm
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),

    # Left leg
    (23, 25), (25, 27), (27, 29), (29, 31), (27, 31),

    # Right leg
    (24, 26), (26, 28), (28, 30), (30, 32), (28, 32),

    # Head (simplified)
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
]

# ============================================================
# Drawing helpers
# ============================================================
def draw_pose_skeleton(frame_bgr, landmarks, min_visibility=0.5):
    h, w = frame_bgr.shape[:2]
    points = []

    for lm in landmarks:
        if hasattr(lm, "visibility") and lm.visibility is not None and lm.visibility < min_visibility:
            points.append(None)
            continue
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((x, y))

    # Draw bones
    for a, b in POSE_CONNECTIONS:
        if a < len(points) and b < len(points) and points[a] and points[b]:
            cv2.line(frame_bgr, points[a], points[b], (0, 255, 0), 2)

    # Draw joints
    for p in points:
        if p:
            cv2.circle(frame_bgr, p, 3, (0, 255, 255), -1)

# ============================================================
# Fall detector
# ============================================================
class FallDetector:
    def __init__(self):
        self.prev_t = None
        self.prev_hip_y = None
        self.state = "OK"
        self.trigger_time = None

        # Balanced MVP thresholds (less sensitive)
        self.hip_drop_vy_thresh = 0.55
        self.shock_drop_thresh = 0.12
        self.shock_window_sec = 0.30

        self.low_hip_y_thresh = 0.72
        self.confirm_seconds = 0.45

    def _vis_ok(self, lm, min_vis=0.4):
        return (not hasattr(lm, "visibility")) or (lm.visibility is None) or (lm.visibility >= min_vis)

    def update(self, landmarks):
        now = time.time()
        if self.prev_t is None:
            self.prev_t = now

        dt = max(1e-3, now - self.prev_t)

        lh, rh = landmarks[23], landmarks[24]

        info = {
            "state": self.state,
            "hip_y": None,
            "hip_vy": 0.0,
            "fast_drop": False,
            "shock_drop": False,
            "low_to_ground": False,
            "reason": None,
        }

        if not (self._vis_ok(lh) and self._vis_ok(rh)):
            self.prev_t = now
            info["reason"] = "low_visibility"
            return False, info

        hip_y = (lh.y + rh.y) / 2.0

        hip_vy = 0.0
        if self.prev_hip_y is not None:
            hip_vy = (hip_y - self.prev_hip_y) / dt  # positive means moving DOWN in image coords

        fast_drop = hip_vy > self.hip_drop_vy_thresh

        shock_drop = False
        if self.prev_hip_y is not None and dt <= self.shock_window_sec:
            shock_drop = (hip_y - self.prev_hip_y) > self.shock_drop_thresh

        low_to_ground = hip_y > self.low_hip_y_thresh

        fell = False

        if self.state == "OK":
            if shock_drop or (fast_drop and hip_y > 0.55):
                self.state = "POSSIBLE_FALL"
                self.trigger_time = now

        elif self.state == "POSSIBLE_FALL":
            if low_to_ground and self.trigger_time is not None:
                if (now - self.trigger_time) >= self.confirm_seconds:
                    self.state = "FALL_CONFIRMED"
                    fell = True
            elif (not fast_drop) and (not low_to_ground) and self.trigger_time is not None and (now - self.trigger_time) > 0.9:
                self.state = "OK"
                self.trigger_time = None

        elif self.state == "FALL_CONFIRMED":
            # one-shot
            self.state = "OK"
            self.trigger_time = None

        self.prev_t = now
        self.prev_hip_y = hip_y

        info.update({
            "state": self.state,
            "hip_y": hip_y,
            "hip_vy": hip_vy,
            "fast_drop": fast_drop,
            "shock_drop": shock_drop,
            "low_to_ground": low_to_ground,
        })

        return fell, info

# ============================================================
# Main loop (THIS is what you import!)
# ============================================================
def run_pose_skeleton(camera_index: int = 0, stop_event: threading.Event | None = None) -> bool:
    """
    Runs pose skeleton + fall detection.

    Returns:
      True  -> fall confirmed
      False -> exited for other reason (q pressed / camera ended / stop_event set externally)

    Behavior:
      - If fall confirmed, sets stop_event (if provided) and exits.
      - If stop_event is set externally (wake word), exits cleanly.
    """
    base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.6,
        min_pose_presence_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    landmarker = vision.PoseLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        landmarker.close()
        raise RuntimeError("Could not open camera")

    fall_detector = FallDetector()
    start_time = time.time()
    fell_triggered = False

    try:
        while True:
            if stop_event is not None and stop_event.is_set():
                break

            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            timestamp_ms = int((time.time() - start_time) * 1000)
            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            if result.pose_landmarks:
                draw_pose_skeleton(frame, result.pose_landmarks[0])
                fell, info = fall_detector.update(result.pose_landmarks[0])

                if fell:
                    fell_triggered = True
                    cv2.putText(frame, "FALL DETECTED!", (30, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    if stop_event is not None:
                        stop_event.set()
                    # show the frame for a moment if you want; otherwise exit immediately
                    # cv2.imshow("MediaPipe Pose Skeleton", frame); cv2.waitKey(1)
                    break

                cv2.putText(
                    frame,
                    f'{info.get("state","?")} vy={info.get("hip_vy",0.0):.2f}',
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )
            else:
                cv2.putText(frame, "No pose", (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("MediaPipe Pose Skeleton", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                if stop_event is not None:
                    stop_event.set()
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        landmarker.close()

    return fell_triggered


if __name__ == "__main__":
    # Local test
    run_pose_skeleton()

