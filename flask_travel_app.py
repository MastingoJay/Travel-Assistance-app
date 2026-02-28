import os
import json
from dotenv import load_dotenv
from groq import Groq
from flask import Flask, render_template, request, jsonify

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# GLOBAL MEMORY
past_trips = [] 

SYSTEM_PROMPT = """
You are an AI travel planner agent.
You MUST return valid JSON following this exact schema:
{
  "destination": "string",
  "duration_days": number,
  "travel_style": "budget | mid-range | luxury",
  "daily_plan": [{"day": number, "title": "string", "activities": ["string"]}],
  "estimated_budget_usd": number,
  "tips": ["string"]
}
Rules: No markdown, no explanations, strictly JSON.
"""

# --- YOUR TOOLS ---
def get_weather(city):
    return f"The weather in {city} will be sunny, 25°C"

def estimate_budget(trip_days, style):
    rates = {"budget": 50, "mid-range": 100, "luxury": 250}
    return trip_days * rates.get(style, 100)

# --- ROUTES ---
@app.route("/", methods=["GET"])
def index():
    # This simply loads your index.html file from the /templates folder
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Use request.json because your index.html JS sends JSON
    data = request.json
    if not data or "trip_request" not in data:
        return jsonify({"error": "Missing trip_request"}), 400
        
    user_input = data.get("trip_request", "")

    # 1. KEYWORD RAG
    relevant_trips = []
    for trip in past_trips:
        if any(word.lower() in user_input.lower() for word in trip.get("destination", "").split()):
            relevant_trips.append(trip)

    context_texts = "\n".join([json.dumps(trip) for trip in relevant_trips])

    # 2. PROMPT BUILDING
    prompt = SYSTEM_PROMPT
    if context_texts:
        prompt += "\n\nPrevious trips for reference:\n" + context_texts
    prompt += "\n\nUser query: " + user_input

    # 3. FAST GROQ CALL
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        
        raw_output = response.choices[0].message.content
        
        # Clean potential markdown backticks
        clean_json = raw_output.replace("```json", "").replace("```", "").strip()
        itinerary = json.loads(clean_json)

        # 4. APPLY TOOLS
        itinerary["tips"].append(get_weather(itinerary["destination"]))
        itinerary["estimated_budget_usd"] = estimate_budget(
            itinerary["duration_days"],
            itinerary["travel_style"]
        )

        # 5. SAVE TO MEMORY
        past_trips.append(itinerary)

        return jsonify(itinerary)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)