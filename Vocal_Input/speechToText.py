import speech_recognition as sr
import re
from typing import List, Optional

# ===============================
# Shared recognizer (IMPORTANT)
# ===============================
_r = sr.Recognizer()

# Wake-word tuning (short phrases)
_r.dynamic_energy_threshold = False
_r.energy_threshold = 220          # tweak 160–300 if needed
_r.pause_threshold = 0.65
_r.phrase_threshold = 0.05
_r.non_speaking_duration = 0.30

# ===============================
# Wake-word helpers
# ===============================
_HEY_WORDS = {"hey", "hi", "ok", "okay"}

# What Google commonly outputs instead of "cam"
_CAM_LIKELY = {
    "cam", "camm", "cammy", "cameron",
    "can", "cap", "cal", "came", "camp",
    "ham", "sam", "tam", "kim", "ken",
}

def _normalize(t: str) -> str:
    t = t.lower().strip()
    t = re.sub(r"[^a-z\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t

def _extract_transcripts(show_all_result) -> List[str]:
    transcripts: List[str] = []
    if isinstance(show_all_result, dict):
        for alt in show_all_result.get("alternative", []):
            tr = alt.get("transcript")
            if tr:
                transcripts.append(tr)
    elif isinstance(show_all_result, str):
        transcripts.append(show_all_result)
    return transcripts

def _is_wake(transcript: str) -> bool:
    t = _normalize(transcript)
    tokens = t.split()
    if not tokens:
        return False

    # Handle glued forms like "heycam"
    glued = t.replace(" ", "")
    if "heycam" in glued or "hicam" in glued:
        return True

    # Prefer: hey + cam-like token
    for i, tok in enumerate(tokens[:4]):
        if tok in _HEY_WORDS:
            for j in (i + 1, i + 2):
                if j < len(tokens) and tokens[j] in _CAM_LIKELY:
                    return True

    # Fallback: hey early + cam-like anywhere early
    if any(w in _HEY_WORDS for w in tokens[:4]) and any(w in _CAM_LIKELY for w in tokens[:8]):
        return True

    return False

# ===============================
# Public API
# ===============================
def detect_wake_word(
    device_index: int | None = None,
    calibrate: bool = True,
    calibration_duration: float = 0.6,
    timeout: float = 3.0,
    phrase_time_limit: float = 2.5,
    language: str = "en-CA",
) -> bool:
    """
    Listens once and returns True if it likely heard "hey cam(m)".
    Prints nothing.
    """
    mic_kwargs = {}
    if device_index is not None:
        mic_kwargs["device_index"] = device_index

    with sr.Microphone(**mic_kwargs) as source:
        if calibrate:
            _r.adjust_for_ambient_noise(source, duration=calibration_duration)
            _r.energy_threshold = max(120, int(_r.energy_threshold * 0.75))

        audio = _r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        result = _r.recognize_google(audio, show_all=True, language=language)
    except sr.UnknownValueError:
        return False

    transcripts = _extract_transcripts(result)
    return any(_is_wake(t) for t in transcripts)

def listen_long_form(
    device_index: int | None = None,
    timeout: float = 8.0,
    phrase_time_limit: float = 12.0,
    language: str = "en-CA",
    lower: bool = True,
) -> Optional[str]:
    """
    Listens for longer speech and returns what was said,
    or None if nothing understandable was detected.
    """
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

# ===============================
# Example usage
# ===============================
while(1):
    try:
        d = detect_wake_word()
        print(d)  

        if d:
            print("Wake detected — listening for command...")
            command = listen_long_form()
            print(command)

    except sr.WaitTimeoutError:
        print(False)
