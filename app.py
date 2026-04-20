"""
AI Interview Voice Bot — Flask Web Server
100% Free Stack: Groq (Llama3) + gTTS + Google Speech Recognition
"""

import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from question_generator import generate_questions
from tts_engine import text_to_speech_base64
from transcriber import transcribe_audio
from feedback_engine import evaluate_response

app = Flask(__name__, static_folder="static")
CORS(app)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio_files")
os.makedirs(AUDIO_DIR, exist_ok=True)


# ── Health check ──────────────────────────────────────────
@app.route("/api/health")
def health():
    key_set = bool(os.environ.get("GROQ_API_KEY"))
    return jsonify({"status": "ok", "groq_key_set": key_set})


# ── Serve the frontend ────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ── Step 1 + 2: Generate questions + TTS audio ────────────
@app.route("/api/generate-questions", methods=["POST"])
def api_generate_questions():
    data = request.json
    profile = data.get("profile", "").strip()

    if not profile:
        return jsonify({"error": "Profile is required"}), 400

    if not os.environ.get("GROQ_API_KEY"):
        return jsonify({"error": "GROQ_API_KEY is not set. Get free key at console.groq.com"}), 500

    try:
        questions = generate_questions(profile)
        questions_with_audio = []
        for i, q in enumerate(questions):
            audio_b64 = text_to_speech_base64(q)
            questions_with_audio.append({
                "index": i,
                "question": q,
                "audio_b64": audio_b64
            })
        return jsonify({"questions": questions_with_audio})
    except Exception as e:
        print(f"ERROR in generate_questions: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ── Step 3 + 4: Transcribe recorded audio ─────────────────
@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".webm", dir=AUDIO_DIR
    ) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        transcript = transcribe_audio(tmp_path)
        return jsonify({"transcript": transcript})
    except Exception as e:
        print(f"ERROR in transcribe: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ── Step 5: AI Feedback ───────────────────────────────────
@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    data = request.json
    question   = data.get("question", "")
    transcript = data.get("transcript", "")

    if not question or not transcript:
        return jsonify({"error": "question and transcript are required"}), 400

    try:
        feedback = evaluate_response(question, transcript)
        return jsonify(feedback)
    except Exception as e:
        print(f"ERROR in feedback: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("\n⚠️  WARNING: GROQ_API_KEY is not set!")
        print("   Get your free key at: https://console.groq.com")
        print("   Then run: $env:GROQ_API_KEY='your-key-here'\n")
    else:
        print(f"✅ Groq API key loaded (ends in ...{key[-6:]})")

    print("🚀 Starting AI Interview Bot...")
    print("   Open http://localhost:5000 in your browser\n")
    app.run(debug=True, port=5000)