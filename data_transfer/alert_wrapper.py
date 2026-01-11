import threading
from data_transfer import send_fall_alert, send_wake_alert

def wrap_fall_detection(run_pose_skeleton_func):
    """
    Wraps the fall detection function to send alerts
    
    Usage in main.py:
        from data_transfer.alert_wrapper import wrap_fall_detection
        run_pose_skeleton = wrap_fall_detection(run_pose_skeleton)
    """
    def wrapper(camera_id, stop_event):
        result = run_pose_skeleton_func(camera_id, stop_event)
        if result:  # Fall detected
            # Send alert in background to avoid blocking
            threading.Thread(
                target=send_fall_alert,
                kwargs={'location': f'Camera {camera_id}'},
                daemon=True
            ).start()
        return result
    return wrapper

def wrap_wake_word_detection(wait_for_wake_word_func):
    """
    Wraps the wake word detection function to send alerts
    
    Usage in main.py:
        from data_transfer.alert_wrapper import wrap_wake_word_detection
        wait_for_wake_word = wrap_wake_word_detection(wait_for_wake_word)
    """
    def wrapper(stop_event):
        result = wait_for_wake_word_func(stop_event)
        if result:  # Wake word detected
            # Send alert in background to avoid blocking
            threading.Thread(
                target=send_wake_alert,
                daemon=True
            ).start()
        return result
    return wrapper

# Convenience function to wrap both at once
def enable_alert_system(run_pose_skeleton_func, wait_for_wake_word_func):
    """
    Wraps both detection functions with alert sending
    
    Usage in main.py:
        from data_transfer.alert_wrapper import enable_alert_system
        run_pose_skeleton, wait_for_wake_word = enable_alert_system(
            run_pose_skeleton, wait_for_wake_word
        )
    """
    return (
        wrap_fall_detection(run_pose_skeleton_func),
        wrap_wake_word_detection(wait_for_wake_word_func)
    )
