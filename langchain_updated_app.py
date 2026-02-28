import os
import json
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# Load API key
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
You are an AI travel planner agent.

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
- Use tools if needed (Weather, Budget)
- Do not include explanations
- Do not include markdown
- Do not include text outside JSON
- Always fill all fields
"""

# -----------------------------
# Example Tools
# -----------------------------
def get_weather(city):
    # Placeholder stub (replace with real API later)
    return f"The weather in {city} will be sunny, 25°C"

def estimate_budget(trip_days, style):
    rates = {"budget": 50, "mid-range": 100, "luxury": 250}
    return trip_days * rates.get(style, 100)

# -----------------------------
# Interactive travel planner
# -----------------------------
print("🧠 Travel Agent with Tools — type 'exit' to quit\n")

while True:
    user_input = input("Trip request: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Safe travels.")
        break

    # 1️⃣ Ask AI for plan
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    raw_output = response.choices[0].message.content

    # 2️⃣ Parse JSON
    try:
        itinerary = json.loads(raw_output)

        # 3️⃣ Apply tools automatically
        # Weather for destination
        itinerary["tips"].append(get_weather(itinerary["destination"]))

        # Budget calculation
        itinerary["estimated_budget_usd"] = estimate_budget(
            itinerary["duration_days"],
            itinerary["travel_style"]
        )

        # 4️⃣ Print full structured itinerary
        print("\n📋 Structured Itinerary with Tools:\n")
        print(json.dumps(itinerary, indent=2))

    except json.JSONDecodeError:
        print("\n⚠️ Model returned invalid JSON:")
        print(raw_output)