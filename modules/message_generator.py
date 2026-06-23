from random import choice
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY
)

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

FALLBACK_MESSAGES = [
    "Interesting movement lately. Curious how it develops.",
    "This one is getting attention recently.",
    "Market activity looks notable here.",
    "Worth keeping an eye on this."
]


def build_prompt(coin):
    return f"""
Coin: {coin.get("name")}
Symbol: {coin.get("symbol")}
Price: {coin.get("price")}
24h Change: {coin.get("change_24h")}
Market Cap: {coin.get("market_cap")}
Volume: {coin.get("volume_24h")}

Write a short 1-2 sentence human-like CoinMarketCap community message.

Rules:
- Natural tone.
- No emojis.
- No hashtags.
- No financial advice.
- Output only the message.
""".strip()


def call_openai(prompt):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=80
    )

    return response.choices[0].message.content.strip()


# def call_gemini(prompt):
#     ...

# def call_groq(prompt):
#     ...


def generate_message(coin):

    prompt = build_prompt(coin)

    try:

        text = call_openai(prompt)

        if text and len(text) > 15:
            return text

    except Exception as e:

        print(
            "OpenAI failed:",
            e
        )

    return choice(
        FALLBACK_MESSAGES
    )


if __name__ == "__main__":

    sample = {
        "name": "Bitcoin",
        "symbol": "BTC",
        "price": "$63,000",
        "change_24h": "1.2%",
        "market_cap": "$1.2T",
        "volume_24h": "$18B"
    }

    print(
        generate_message(sample)
    )
