from playwright.sync_api import sync_playwright

# ----------------- Session Management -----------------
'''
This module provides functions to manage browser sessions using Playwright.
Functions:
    - check_login: Checks if the user is logged in to CoinMarketCap by verifying the
    presence of the post button on a specific coin's page.
    - The function returns a dictionary indicating the login status and any relevant messages.
    - The function handles exceptions and returns an error message if any issues occur during the process.
'''
def check_login():

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