import asyncio
from playwright.async_api import async_playwright
import requests

BOT_TOKEN = "8534355535:AAGbinmoIRFlp3kBmDcDuND_4v99RupruTM"
CHAT_ID = "YOUR_CHAT_ID"     # <-- yaha apna chat id daalna hai

PRODUCTS = {
    "iPhone 17 White 256GB": 
        "https://www.croma.com/apple-iphone-17-256gb-white-/p/317398",

    "Vivo T4r 8/128 Arctic White": 
        "https://www.croma.com/vivo-t4r-5g-8gb-ram-128gb-arctic-white-/p/317526",
}

last_status = {name: "OUT" for name in PRODUCTS}


def send_telegram(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
        )
    except:
        pass


async def check_stock(playwright, url):
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    await page.goto(url, timeout=60000)
    html = await page.content()
    await browser.close()

    return "IN" if '"skuStockFlag":true' in html else "OUT"


async def main_loop():
    print("🔥 Railway Playwright Croma Tracker Started...")

    async with async_playwright() as p:
        while True:
            for name, url in PRODUCTS.items():
                status = await check_stock(p, url)
                print(name, "=>", status)

                if last_status[name] == "OUT" and status == "IN":
                    send_telegram(f"🔥 IN STOCK!\n{name}\n{url}")

                last_status[name] = status

            print("-" * 40)
            await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main_loop())
