import speech_recognition as sr
import re
import threading
import time
from typing import Optional

TESTING = True

_r = sr.Recognizer()

# ---- TUNING: better for short 2-word wake phrases ----
_r.dynamic_energy_threshold = True
_r.dynamic_energy_adjustment_damping = 0.15
_r.dynamic_energy_ratio = 1.7

_r.pause_threshold = 0.35          # was 0.65; stop less "late"
_r.phrase_threshold = 0.10         # require a little speech
_r.non_speaking_duration = 0.15    # trim silence

_HEY_WORDS = {"hey", "hi", "ok", "okay"}
_AMPM = {"am", "pm"}

_CAM_LIKELY = {
    "cam", "camm", "cammy", "cameron",
    "can", "cap", "cal", "came", "camp",
    "ham", "sam", "tam", "kim", "ken",
    "8", "8am", "8pm", "8m", "800",
}

def _normalize(t: str) -> str:
    t = t.lower().strip()
    t = re.sub(r"[^a-z0-9\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t

def _is_wake_text(text: str) -> bool:
    t = _normalize(text)
    tokens = t.split()
    glued = t.replace(" ", "")

    if not tokens:
        return False

    # glued forms
    if "heycam" in glued or "hicam" in glued:
        return True

    # need a hey-word early (keeps false positives down)
    has_hey = any(w in _HEY_WORDS for w in tokens[:4])
    if not has_hey:
        return False

    # direct cam-like token soon after
    if any(w in _CAM_LIKELY for w in tokens[:8]):
        # if we literally got "hey can"/"hey cam" etc
        return True

    # time-ish patterns: "8 am"/"8 pm"/"8 m"/"8 mm"/"800 am"
    scan = tokens[:10]
    for i, tok in enumerate(scan):
        if tok == "8":
            if i + 1 < len(scan) and scan[i + 1] in _AMPM:
                return True
            if i + 1 < len(scan) and scan[i + 1] == "m":
                return True
            if i + 1 < len(scan) and scan[i + 1] == "mm":
                return True
        if tok == "800" and i + 1 < len(scan) and scan[i + 1] in _AMPM:
            return True
        if tok in {"8am", "8pm", "8m"}:
            return True

    return False

def calibrate_mic(device_index: int | None = None, duration: float = 1.2) -> None:
    mic_kwargs = {}
    if device_index is not None:
        mic_kwargs["device_index"] = device_index
    with sr.Microphone(**mic_kwargs) as source:
        _r.adjust_for_ambient_noise(source, duration=duration)

def detect_wake_word(
    device_index: int | None = None,
    calibrate: bool = False,
    calibration_duration: float = 1.2,
    timeout: float = 4.0,
    phrase_time_limit: float = 2.8,   # IMPORTANT: longer so it catches "hey cam"
    language: str = "en-CA",
) -> bool:
    mic_kwargs = {}
    if device_index is not None:
        mic_kwargs["device_index"] = device_index

    with sr.Microphone(**mic_kwargs) as source:
        if calibrate:
            _r.adjust_for_ambient_noise(source, duration=calibration_duration)

        audio = _r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        # ---- KEY CHANGE: use single best transcript (NOT show_all) ----
        text = _r.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        if TESTING:
            print(["<UnknownValueError>"])
        return False
    except sr.RequestError:
        if TESTING:
            print(["<RequestError>"])
        return False

    hit = _is_wake_text(text)

    if TESTING:
        print([text], "hit=", hit)

    return hit

def listen_long_form(
    device_index: int | None = None,
    timeout: float = 8.0,
    phrase_time_limit: float = 12.0,
    language: str = "en-CA",
    lower: bool = True,
) -> Optional[str]:
    mic_kwargs = {}
    if device_index is not None:
        mic_kwargs["device_index"] = device_index

    with sr.Microphone(**mic_kwargs) as source:
        audio = _r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        text = _r.recognize_google(audio, language=language).strip()
        return text.lower() if lower else text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def wait_for_wake_word(
    stop_event: threading.Event,
    device_index: int | None = None,
    language: str = "en-CA",
    calibrate_once: bool = True,
    calibration_duration: float = 1.2,
    sleep_s: float = 0.02,
) -> bool:
    if calibrate_once:
        calibrate_mic(device_index=device_index, duration=calibration_duration)

    while not stop_event.is_set():
        try:
            hit = detect_wake_word(
                device_index=device_index,
                calibrate=False,
                timeout=4.0,
                phrase_time_limit=2.8,
                language=language,
            )
            if hit:
                stop_event.set()
                return True
        except sr.WaitTimeoutError:
            pass
        time.sleep(sleep_s)

    return False

if __name__ == "__main__" and TESTING:
    calibrate_mic(duration=1.2)
    while True:
        try:
            print("wake:", detect_wake_word())
        except sr.WaitTimeoutError:
            print("wake: False")
