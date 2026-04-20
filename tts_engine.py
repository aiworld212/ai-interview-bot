"""
Step 2: The Voice of the Interviewer (Text-to-Speech)
Uses gTTS (Google Text-to-Speech) — completely FREE, no API key needed.
"""

import os
import base64
import tempfile
from gtts import gTTS


def text_to_speech_base64(text: str, lang: str = "en") -> str:
    """
    Converts text to speech and returns base64-encoded MP3 for the web browser.

    Args:
        text: The question text to speak.
        lang: Language code (default 'en').

    Returns:
        Base64-encoded MP3 string.
    """
    tts = gTTS(text=text, lang=lang, slow=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode("utf-8")
    finally:
        os.unlink(tmp_path)


def text_to_speech_file(text: str, output_path: str, lang: str = "en") -> str:
    """
    Converts text to speech and saves as an MP3 file.

    Args:
        text: The question text to speak.
        output_path: Where to save the MP3.
        lang: Language code.

    Returns:
        The output file path.
    """
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(output_path)
    return output_path


def batch_text_to_speech(questions: list, output_dir: str) -> list:
    """
    Converts a list of questions to individual MP3 files.

    Args:
        questions: List of question strings.
        output_dir: Directory to save MP3s.

    Returns:
        List of saved file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for i, q in enumerate(questions):
        path = os.path.join(output_dir, f"question_{i + 1}.mp3")
        text_to_speech_file(q, path)
        paths.append(path)
        print(f"✅ Saved: {path}")
    return paths


if __name__ == "__main__":
    b64 = text_to_speech_base64("Tell me about a time you handled a tight deadline.")
    print(f"Base64 audio generated ({len(b64)} chars)")
