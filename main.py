import threading
from Body.body import run_pose_skeleton
from Vocal_Input.speechToText import wait_for_wake_word
from Vocal_Input.speechToText import calibrate_mic

calibrate_mic(duration=0.8)  # do once at startup

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
            print("Fall detected — emergency logic here")

if __name__ == "__main__":
    main()


