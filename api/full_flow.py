from fastapi import APIRouter

from modules.fetch_trending import fetch_trending_coins
from modules.message_generator import generate_message
from modules.chat_poster import (
    create_browser_session,
    close_browser_session,
    post_chat_with_session
)

router = APIRouter()


@router.post("/full-flow")
def full_flow():

    try:

        # If we already scraped recently (e.g., during debugging), reuse it.
        # This avoids re-running the Playwright scraping step every time /full-flow is called.
        try:
            import json, os
            # default path if not set yet
            if "last_trending_path" not in locals():
                last_trending_path = "output/last_trending.json"

            if os.path.exists(last_trending_path):
                with open(last_trending_path, "r", encoding="utf-8") as f:
                    coins = json.load(f)
            else:
                coins = fetch_trending_coins()
        except Exception:
            coins = fetch_trending_coins()

        # Persist scraped trending coins for this run so we do not scrape again
        # if the endpoint is re-invoked while debugging.
        # (Also makes it possible to inspect inputs used for message generation.)
        try:
            import os, json
            os.makedirs("output", exist_ok=True)
            with open("output/last_trending.json", "w", encoding="utf-8") as f:
                json.dump(coins, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        results = []

        success_count = 0

        failed_count = 0

        output_results_path = "output/results.json"
        last_trending_path = "output/last_trending.json"

        session = create_browser_session(storage_state_path="auth/state.json", headless=False)

        for coin in coins:


            try:

                # Avoid repeating fallback messages: if generator returns a known fallback,
                # retry once using a slightly different prompt.
                message = generate_message(coin)

                # Simple repeat protection: if the LLM failed and we got a too-short/common fallback,
                # retry once.
                if not message or len(message) < 20:
                    message = generate_message(coin)

                response = post_chat_with_session(
                    session=session,
                    coin_url=coin["url"],
                    message=message,
                    sentiment="bullish"
                )

                if response["status"] == "success":

                    success_count += 1

                else:

                    failed_count += 1

                results.append(
                    {
                        "url": coin["url"],
                        "message": message,
                        "status": response["status"]
                    }
                )

            except Exception as e:

                failed_count += 1

                results.append(
                    {
                        "url": coin["url"],
                        "status": "error",
                        "message": str(e)
                    }
                )

        import json

        output = {

            "status": "completed",

            "total_coins": len(coins),

            "success_count": success_count,

            "failed_count": failed_count,

            "results": results
        }

        try:

            with open(output_results_path, "w", encoding="utf-8") as f:

                json.dump(output, f, ensure_ascii=False, indent=2)

        except Exception:

            pass

        return output

    except Exception as e:

        return {

            "status": "error",

            "message": str(e)
        }

    finally:

        try:
            close_browser_session(session)
        except Exception:
            pass

