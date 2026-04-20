import json
import os
from groq import Groq

client_groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_questions(profile: str) -> list:
    prompt = f"""You are an expert technical interviewer.

Given this candidate profile, generate exactly 5 behavioral interview questions.

CANDIDATE PROFILE:
{profile}

REQUIREMENTS:
- Focus on soft skills in technical context
- Start with Tell me about a time or Describe a situation
- Cover deadlines, teamwork, failure, explaining code, learning

Respond ONLY with a valid JSON array of exactly 5 strings. No extra text.
Example: ["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]
"""

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]).strip()

    questions = json.loads(text)
    return [str(q) for q in questions]