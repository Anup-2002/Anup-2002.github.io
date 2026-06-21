import random
import time

from playwright.sync_api import (
    sync_playwright
)


def verify_session():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        try:

            context = browser.new_context(
                storage_state="auth/state.json"
            )

            page = context.new_page()

            page.goto(
                "https://coinmarketcap.com/currencies/bitcoin/",
                wait_until="networkidle"
            )

            page.wait_for_timeout(
                3000
            )

            textbox = page.locator(
                '[data-test="base-editor-editable"]'
            )

            if textbox.count() == 0:

                return {
                    "status": "error",
                    "message": "Comment editor not found"
                }

            post_button = page.locator(
                '[data-test="editor-post-button"]'
            )

            if post_button.count() == 0:

                return {
                    "status": "error",
                    "message": "Post button not found"
                }

            text = (
                post_button
                .inner_text()
                .strip()
            )

            if "Log in" in text:

                return {
                    "status": "error",
                    "message": "Session expired"
                }

            return {
                "status": "success",
                "message": "Session active"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

        finally:

            browser.close()


def create_browser_session(storage_state_path="auth/state.json", headless=False):

    p = sync_playwright().start()

    browser = p.chromium.launch(headless=headless)

    context = browser.new_context(storage_state=storage_state_path)

    return {
        "playwright": p,
        "browser": browser,
        "context": context
    }


def close_browser_session(session):

    try:
        session["context"].close()
    except Exception:
        pass

    try:
        session["browser"].close()
    except Exception:
        pass

    try:
        session["playwright"].stop()
    except Exception:
        pass


def post_chat_with_session(
    session,
    coin_url,
    message,
    sentiment="bullish"
):

    page = session["context"].new_page()

    try:

        page.goto(
            coin_url,
            wait_until="networkidle"
        )

        page.wait_for_timeout(
            random.randint(
                3000,
                5000
            )
        )

        textbox = page.locator(
            '[data-test="base-editor-editable"]'
        )

        if textbox.count() == 0:

            return {
                "status": "error",
                "message": "Comment editor not found"
            }

        textbox.click()

        page.keyboard.type(
            message,
            delay=random.randint(
                15,
                40
            )
        )

        page.wait_for_timeout(
            random.randint(
                800,
                1500
            )
        )

        if sentiment.lower() == "bullish":

            button = page.locator(
                '[data-test="editor-bullish-button"]'
            )

        else:

            button = page.locator(
                '[data-test="editor-bearish-button"]'
            )

        if button.count():

            button.click()

        page.wait_for_timeout(
            random.randint(
                500,
                1200
            )
        )

        post_button = page.locator(
            '[data-test="editor-post-button"]'
        )

        if post_button.count() == 0:

            return {
                "status": "error",
                "message": "Post button not found"
            }

        text = (
            post_button
            .inner_text()
            .strip()
        )

        if "Log in" in text:

            return {
                "status": "error",
                "message": "Session expired"
            }

        post_button.click()

        page.wait_for_timeout(
            random.randint(
                4000,
                7000
            )
        )

        try:

            remaining_text = (
                textbox
                .inner_text()
                .strip()
            )

        except:

            remaining_text = ""

        if remaining_text == "":

            return {
                "status": "success",
                "message": "Post submitted"
            }

        return {
            "status": "unknown",
            "message": "Unable to verify post"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

    finally:

        try:
            page.close()
        except Exception:
            pass


def post_chat(
    coin_url,
    message,
    sentiment="bullish"
):

    session = create_browser_session(storage_state_path="auth/state.json", headless=False)

    try:
        return post_chat_with_session(
            session=session,
            coin_url=coin_url,
            message=message,
            sentiment=sentiment
        )
    finally:
        close_browser_session(session)



if __name__ == "__main__":

    result = post_chat(

        coin_url=
        "https://coinmarketcap.com/currencies/bitcoin/",

        message=
        "Interesting activity lately. Curious to see how things develop.",

        sentiment="bullish"

    )

    print(
        result
    )