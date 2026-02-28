import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("🌍 AI Travel Assistant (Groq) — type 'exit' to quit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye! Safe travels.")
        break

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful AI travel assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )

    print("\n✈️ Travel Assistant:")
    print(response.choices[0].message.content)
    print()