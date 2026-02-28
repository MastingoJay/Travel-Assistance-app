import os
import json
from dotenv import load_dotenv
from groq import Groq

# -----------------------------
# Load API key and initialize Groq
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
- Consider past trips and user preferences
- Do not include explanations
- Do not include markdown
- Do not include text outside JSON
- Always fill all fields
"""

# -----------------------------
# Tools
# -----------------------------
def get_weather(city):
    return f"The weather in {city} will be sunny, 25°C"

def estimate_budget(trip_days, style):
    rates = {"budget": 50, "mid-range": 100, "luxury": 250}
    return trip_days * rates.get(style, 100)

# -----------------------------
# In-memory memory / RAG system
# -----------------------------
past_trips = []  # stores previous itineraries

# -----------------------------
# Interactive travel planner
# -----------------------------
print("🧠 Groq Travel Agent with Memory — type 'exit' to quit\n")

while True:
    user_input = input("Trip request: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Safe travels.")
        break

    # -----------------------------
    # Retrieve relevant past trips (RAG-like)
    # -----------------------------
    relevant_trips = []
    for trip in past_trips:
        # simple check: include if any word in the destination matches user query
        if any(word.lower() in user_input.lower() for word in trip.get("destination", "").split()):
            relevant_trips.append(trip)

    context_texts = "\n".join([json.dumps(trip) for trip in relevant_trips])

    # -----------------------------
    # Prepare prompt for Groq
    # -----------------------------
    prompt = SYSTEM_PROMPT
    if context_texts:
        prompt += "\n\nPrevious trips for reference:\n" + context_texts
    prompt += "\n\nUser query: " + user_input

    # -----------------------------
    # Send request to Groq
    # -----------------------------
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )

        raw_output = response.choices[0].message.content

        # -----------------------------
        # Parse JSON
        # -----------------------------
        itinerary = json.loads(raw_output)

        # Apply tools automatically
        itinerary["tips"].append(get_weather(itinerary["destination"]))
        itinerary["estimated_budget_usd"] = estimate_budget(
            itinerary["duration_days"],
            itinerary["travel_style"]
        )

        # Print structured itinerary
        print("\n📋 Structured Itinerary:\n")
        print(json.dumps(itinerary, indent=2))

        # Save itinerary to memory
        past_trips.append(itinerary)

    except json.JSONDecodeError:
        print("\n⚠️ Model returned invalid JSON:")
        print(raw_output)
    except Exception as e:
        print("\n❌ Error communicating with Groq API:")
        print(e)