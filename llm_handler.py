import os
import json
import re
from openai import OpenAI
from openai import RateLimitError
from config import OPEN_AI_API_KEY, OPEN_AI_BASE_URL
from typing import List, Union



client = OpenAI(
    api_key=OPEN_AI_API_KEY,
    base_url=OPEN_AI_BASE_URL
)
# Normalize answers to feed into GPT
def format_answers_for_prompt(answers: List[dict]) -> str:
    formatted = []
    for a in answers:
        formatted.append(f"Q{a.id} : {a.value}")

    return "\n".join(formatted)

def analyze_cultural_personality(answers: List[dict]) -> dict:
    prompt = f"""
You are an expert cultural anthropologist AI. Based on this user's responses to a personality quiz, determine which of the following 8 ancient cultures best aligns with their mindset and values:

- Norse/Viking
- Harappan (Indus Valley)
- Greek (Ancient Greece)
- Yoruba
- Mayan
- Japanese (Zen)
- Renaissance Italian
- Egyptian (Ancient Egypt)

The answers are a mix of multiple-choice values and sliders (on a scale from 0 to 1).

Here are the answers:
{format_answers_for_prompt(answers)}


Return only JSON in this format:
{{
  "cultural_match": "<one of the 8>",
  "confidence": 0.0 to 1.0,
  "key_traits": ["trait1", "trait2", "trait3"],
  "reasoning": "Why this match was chosen in 1-2 sentences",
  "advice": "What general advice should be given to them based on their cultural match"
}}

Make sure Key traits should be small 
Make sure you only return the JSON format and nothing else.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are an insightful cultural psychologist."},
                {"role": "user", "content": prompt}
            ]
        )
        # Parse and return JSON result
        result_text = response.choices[0].message.content.strip()
        # Extract JSON from markdown code blocks if present
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = result_text
        return json.loads(json_str)
    except RateLimitError:
        return {"error": "Something happens please again try tomorrow"}
    except Exception as e:
        return {
            "error": str(e),
            "raw_response": locals().get('result_text', None)
        }