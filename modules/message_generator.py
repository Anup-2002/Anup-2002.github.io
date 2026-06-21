from random import choice
import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


FALLBACK_MESSAGES = [
    "Interesting movement lately. Curious how it develops.",
    "This one is getting attention recently.",
    "Market activity looks notable here.",
    "Worth keeping an eye on this."
]


# -------------------------
# PROMPT (OPTIMIZED)
# -------------------------
def build_prompt(coin):
    return f"""
Coin: {coin.get("name")}
Symbol: {coin.get("symbol")}
Price: {coin.get("price")}
24h Change: {coin.get("change_24h")}
Market Cap: {coin.get("market_cap")}
Volume: {coin.get("volume_24h")}

Write a 1–2 sentence casual crypto community message.
No emojis. No hashtags. No financial advice.
Only output text.
""".strip()

def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()



def call_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 80
    }

    r = requests.post(url, json=payload, headers=headers, timeout=10)

    if r.status_code != 200:
        print("GROQ ERROR:", r.text)
        r.raise_for_status()

    return r.json()["choices"][0]["message"]["content"].strip()

def generate_message(coin):
    prompt = build_prompt(coin)

    try:
        text = call_gemini(prompt)
        if text and len(text) > 15:
            return text
    except Exception as e:
        print("Gemini failed:", e)

    try:
        text = call_groq(prompt)
        if text and len(text) > 15:
            return text
    except Exception as e:
        print("Groq failed:", e)
    return choice(FALLBACK_MESSAGES)



if __name__ == "__main__":
    sample = {
        "name": "Bitcoin",
        "symbol": "BTC",
        "price": "$63,000",
        "change_24h": "1.2%",
        "market_cap": "$1.2T",
        "volume_24h": "$18B"
    }

    print(generate_message(sample))