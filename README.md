# 🎤 AI Interview Warm-Up Bot

An AI-powered behavioral interview practice tool built for BSc IT final year project.

## 🚀 Features
- Generates 5 personalized behavioral interview questions using Groq AI
- Converts questions to speech using Google Text-to-Speech (gTTS)
- Records your spoken answers via browser microphone
- Transcribes answers using Google Speech Recognition
- Evaluates answers using STAR method and gives score out of 10
- Provides 2 specific improvement tips per answer
- Downloads full session report

## 🛠️ Tech Stack
- Python + Flask (backend)
- Groq API with Llama 3 (AI questions + feedback)
- gTTS (text to speech)
- Google Speech Recognition (transcription)
- HTML + CSS + JavaScript (frontend)

## ⚙️ Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Get free API key
Go to https://console.groq.com and create a free API key

### 3. Set API key
$env:GROQ_API_KEY="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"

### 4. Run the app
python app.py

### 5. Open in browser
http://localhost:5000

## 📁 Project Structure
- app.py - Flask web server
- question_generator.py - Generates interview questions using Groq
- tts_engine.py - Converts questions to speech
- transcriber.py - Transcribes spoken answers
- feedback_engine.py - Evaluates answers using STAR method
- static/index.html - Web interface

## 👨‍💻 Built By
BSc IT Third Year Student
Project: AI Interview Voice Bot
