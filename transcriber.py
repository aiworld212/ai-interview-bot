"""
Step 3 & 4: Audio Recording + Transcription
Uses SpeechRecognition with Google Speech API — completely FREE, no API key needed.
"""

import os
import subprocess
import tempfile
import speech_recognition as sr


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file using Google's free Speech Recognition API.
    Automatically converts audio format using ffmpeg if needed.

    Args:
        audio_path: Path to audio file (.webm, .wav, .mp3, etc.)

    Returns:
        Transcribed text string.
    """
    # Convert to WAV (16kHz mono) for best recognition accuracy
    wav_path = audio_path + "_converted.wav"
    converted = False

    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", audio_path,
             "-ar", "16000", "-ac", "1",
             "-f", "wav", wav_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            converted = True
        else:
            wav_path = audio_path  # fallback to original
    except (subprocess.TimeoutExpired, FileNotFoundError):
        wav_path = audio_path  # ffmpeg not available

    try:
        transcript = _google_speech_recognize(wav_path)
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")
    finally:
        if converted and os.path.exists(wav_path):
            os.unlink(wav_path)

    return transcript


def _google_speech_recognize(wav_path: str) -> str:
    """
    Uses the SpeechRecognition library with Google's free Speech API.
    No API key required — uses Google's public endpoint.
    """
    recognizer = sr.Recognizer()

    # Adjust sensitivity for better accuracy
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True

    with sr.AudioFile(wav_path) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text.strip()
    except sr.UnknownValueError:
        return "[Could not understand audio — please speak clearly and try again]"
    except sr.RequestError as e:
        raise RuntimeError(
            f"Google Speech API unavailable: {e}. Check your internet connection."
        )


def record_from_microphone(duration: int = 30, output_path: str = None) -> str:
    """
    Step 3: Records audio from the microphone and saves it.
    Used by the CLI version (web version records in browser).

    Args:
        duration: Max recording duration in seconds.
        output_path: Where to save the WAV file.

    Returns:
        Path to the saved WAV file.
    """
    if output_path is None:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        output_path = tmp.name
        tmp.close()

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone(sample_rate=16000) as source:
            print(f"🎙️  Recording for up to {duration} seconds... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=duration
            )
        with open(output_path, "wb") as f:
            f.write(audio.get_wav_data())
        print("✅ Recording complete!")
        return output_path

    except sr.WaitTimeoutError:
        print("⚠️  No speech detected within timeout.")
        return None
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        return None


def transcribe_from_microphone(duration: int = 30) -> str:
    """
    Convenience: Records from mic and immediately transcribes.
    Used in CLI mode.
    """
    wav_path = record_from_microphone(duration=duration)
    if not wav_path:
        return ""
    try:
        transcript = transcribe_audio(wav_path)
        return transcript
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(f"Transcribing: {path}")
        print(f"Result: {transcribe_audio(path)}")
    else:
        print("Recording from microphone...")
        text = transcribe_from_microphone(duration=15)
        print(f"You said: {text}")
