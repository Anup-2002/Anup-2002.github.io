from playwright.sync_api import sync_playwright

# ----------------- Fetch Trending Coins -----------------
'''
This module fetches trending coins from CoinMarketCap using Playwright.
Functions:
    - fetch_trending_coins: Fetches the top trending coins and their details.
    - The function returns a list of dictionaries containing information about each trending coin.
    - Each dictionary includes the coin's name, symbol, price, changes, market cap, volume, liquidity, chain, age, transactions, and URL.        
        
'''

def fetch_trending_coins():

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
                "https://coinmarketcap.com/trending-cryptocurrencies/",
                wait_until="networkidle"
            )

            rows = page.locator(
                "tbody tr"
            )

            coins = []

            count = rows.count()

            for i in range(count):

                if len(coins) == 10:
                    break

                try:

                    row = rows.nth(i)

                    columns = row.locator(
                        "td"
                    )

                    coin_link = row.locator(
                        'a[href^="/currencies/"]'
                    )

                    if coin_link.count() == 0:
                        continue

                    href = coin_link.first.get_attribute(
                        "href"
                    )

                    if not href:
                        continue

                    url = (
                        "https://coinmarketcap.com"
                        + href
                    )

                    name_block = columns.nth(
                        2
                    ).inner_text().split(
                        "\n"
                    )

                    name = name_block[0].strip()

                    symbol = ""

                    for item in name_block:

                        item = item.strip()

                        if (
                            item.isupper()
                            and len(item) <= 10
                            and item != "BUY"
                        ):

                            symbol = item

                            break

                    # -------- Price --------

                    price = columns.nth(
                        3
                    ).inner_text().strip()

                    # -------- Changes --------

                    change_1h = columns.nth(
                        4
                    ).inner_text().strip()

                    change_24h = columns.nth(
                        5
                    ).inner_text().strip()

                    # -------- Market Cap --------

                    market_cap = columns.nth(
                        6
                    ).inner_text().strip()

                    # -------- Volume --------

                    volume_24h = columns.nth(
                        7
                    ).inner_text().strip()

                    # -------- Liquidity + Chain --------

                    liquidity_block = columns.nth(
                        8
                    ).inner_text().split(
                        "\n"
                    )

                    dex_liquidity = ""

                    chain = ""

                    if len(liquidity_block) > 0:

                        dex_liquidity = liquidity_block[
                            0
                        ].strip()

                    if len(liquidity_block) > 1:

                        chain = liquidity_block[
                            -1
                        ].strip()

                    # -------- Age --------

                    age = columns.nth(
                        9
                    ).inner_text().strip()

                    # -------- Transactions --------

                    txns_raw = columns.nth(
                        10
                    ).inner_text()

                    txns = (
                        txns_raw
                        .replace("/", "\n")
                        .split("\n")
                    )

                    txns = [

                        x.strip()

                        for x in txns

                        if x.strip()

                    ]

                    buys_24h = ""

                    sells_24h = ""

                    total_txns_24h = ""

                    numeric_values = []

                    for x in txns:

                        if (
                            any(
                                c.isdigit()
                                for c in x
                            )
                        ):

                            numeric_values.append(
                                x
                            )

                    if len(numeric_values) >= 1:

                        buys_24h = numeric_values[0]

                    if len(numeric_values) >= 2:

                        sells_24h = numeric_values[1]

                    if len(numeric_values) >= 3:

                        total_txns_24h = numeric_values[-1]

                    coins.append(

                        {

                            "name": name,

                            "symbol": symbol,

                            "price": price,

                            "change_1h": change_1h,

                            "change_24h": change_24h,

                            "market_cap": market_cap,

                            "volume_24h": volume_24h,

                            "dex_liquidity": dex_liquidity,

                            "chain": chain,

                            "age": age,

                            "buys_24h": buys_24h,

                            "sells_24h": sells_24h,

                            "total_txns_24h": total_txns_24h,

                            "url": url

                        }

                    )

                except Exception as e:

                    print(
                        f"Skipping row {i}: {e}"
                    )

            return coins

        finally:

            browser.close()


if __name__ == "__main__":

    coins = fetch_trending_coins()

    for coin in coins:

        print(coin)