import json
import os
from groq import Groq

client_groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def evaluate_response(question: str, transcript: str) -> dict:
    prompt = f"""You are an expert interview coach.

QUESTION: {question}
CANDIDATE ANSWER: {transcript}

Evaluate using STAR method. Respond ONLY with valid JSON, no markdown:
{{
  "score": <1-10>,
  "star_breakdown": {{
    "situation": "<assessment>",
    "task": "<assessment>",
    "action": "<assessment>",
    "result": "<assessment>"
  }},
  "clarity_tone": "<2-3 sentences>",
  "tips": ["<tip 1>", "<tip 2>"],
  "overall_summary": "<1-2 sentences>"
}}
"""

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]).strip()

    feedback = json.loads(text)
    feedback["score"] = max(1, min(10, int(feedback["score"])))
    return feedback


def format_feedback_console(feedback: dict, question: str) -> str:
    lines = [
        "=" * 60,
        f"SCORE: {feedback['score']}/10",
        f"Situation: {feedback['star_breakdown']['situation']}",
        f"Task: {feedback['star_breakdown']['task']}",
        f"Action: {feedback['star_breakdown']['action']}",
        f"Result: {feedback['star_breakdown']['result']}",
        f"Clarity: {feedback['clarity_tone']}",
        f"Tip 1: {feedback['tips'][0]}",
        f"Tip 2: {feedback['tips'][1]}",
        f"Summary: {feedback['overall_summary']}",
        "=" * 60,
    ]
    return "\n".join(lines)