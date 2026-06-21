from playwright.sync_api import sync_playwright


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