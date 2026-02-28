import os
import json
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# Load API key and initialize
# -----------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file!")

client = Groq(api_key=api_key)

# -----------------------------
# System prompt / Output schema
# -----------------------------
SYSTEM_PROMPT = """
You are an AI travel planner.

You MUST return valid JSON following this exact schema:

{
  "destination": "string",
  "duration_days": number,
  "travel_style": "budget | mid-range | luxury",
  "daily_plan": [
    {
      "day": number,
      "title": "string",
      "activities": ["string"]
    }
  ],
  "estimated_budget_usd": number,
  "tips": ["string"]
}

Rules:
- Do not include explanations
- Do not include markdown
- Do not include text outside JSON
- Always fill all fields
"""

# -----------------------------
# Interactive travel planner
# -----------------------------
print("🧠 Travel Planner — type 'exit' to quit\n")

while True:
    user_input = input("Trip request: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Safe travels.")
        break

    print("📤 Sending request to AI…")

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Valid Groq model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content

        # Parse JSON
        try:
            itinerary = json.loads(raw_output)
            print("\n📋 Structured Itinerary:\n")
            print(json.dumps(itinerary, indent=2))
        except json.JSONDecodeError:
            print("\n⚠️ Model returned invalid JSON:")
            print(raw_output)

    except Exception as e:
        print("\n❌ Error communicating with Groq API:")
        print(e)