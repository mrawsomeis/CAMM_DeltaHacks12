import os
import sys
from contextlib import contextmanager

@contextmanager
def suppress_native_stderr(enabled: bool = True):
    """
    Silences C/C++ libraries that write directly to stderr (fd=2),
    including MediaPipe / TFLite / absl logs.
    """
    if not enabled:
        yield
        return

    old_fd = os.dup(2)
    try:
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, 2)
        os.close(devnull_fd)

        yield
    finally:
        # Restore stderr
        os.dup2(old_fd, 2)
        os.close(old_fd)

with suppress_native_stderr(True):
    from Body.body import run_pose_skeleton
    from Vocal_Input.speechToText import wait_for_wake_word, calibrate_mic
    from Vocal_Output.labs import speak
    from Hands.hand import hand_moved   
    from Perception.check_status import check_hand_and_face
    from moorcheh.get_alerts import generate_alert_message
    from location.get_location import get_laptop_location_ip
    from location.reverse_geocode import reverse_geocode

import threading

ip = get_laptop_location_ip
loc = reverse_geocode(ip["lat"], ip["lng"])
mes = generate_alert_message(None, loc)
print(mes)

#Toggle API
presentation = False
calibrate_mic(duration=0.8)

def present(s):
    if presentation:
        speak(s)
    else:
        print(s)

def main():
    while True:
        stop_event = threading.Event()
        trigger = {"source": None}

        def wake_wrapper():
            hit = wait_for_wake_word(stop_event)
            if hit and trigger["source"] is None:
                trigger["source"] = "wake"

        def fall_wrapper():
            fell = run_pose_skeleton(0, stop_event)
            if fell and trigger["source"] is None:
                trigger["source"] = "fall"

        wake_thread = threading.Thread(target=wake_wrapper, daemon=True)
        fall_thread = threading.Thread(target=fall_wrapper, daemon=True)

        wake_thread.start()
        fall_thread.start()

        stop_event.wait()

        wake_thread.join(timeout=1)
        fall_thread.join(timeout=1)

        print("Stopped by:", trigger["source"])
        if trigger["source"] == "wake":
            print("Wake word detected — listening for command")

        elif trigger["source"] == "fall":
            triggerMessage = "Hello, I am an automated wellness device, and I have detected a fall. If you are okay, please move your hand."
            present(triggerMessage)
            
            res = check_hand_and_face(
                seconds=3.0,
                camera_index=0,
                face_dir="Face",                  # <-- set to where trained_model.yml is
                require_recognized_face=False,    # True if you ONLY want known people
                show_window=False,
            )

            print("presence:", res.status, "hand:", res.saw_hand, "face:", res.saw_face, "id:", res.face_id)

            if res.status in ("both", "hand_only", "face_only"):
                present("Thank you. I detected a response. I will stand by.")
            else:
                present("I did not detect a hand or face. I am escalating now.")

if __name__ == "__main__":
    main()


