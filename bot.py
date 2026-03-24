import os
import asyncio
import requests
import pandas as pd
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def get_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"

        response = requests.get(url)

        if response.status_code != 200:
            print("API Status Error:", response.status_code)
            return None

        data = response.json()

        prices = data.get("prices", [])

        if not prices:
            print("No data")
            return None

        df = pd.DataFrame(prices, columns=["time", "price"])
        df["price"] = df["price"].astype(float)

        return df

    except Exception as e:
        print("API Error:", e)
        return None


def add_rsi(df):
    delta = df["price"].diff()

    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()

    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


def generate_signal(df):
    if df is None or len(df) < 20:
        return None

    last_rsi = df["rsi"].iloc[-1]

    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    return None


async def main():
    print("Bot started...")

    while True:
        try:
            df = get_data()

            if df is None:
                await asyncio.sleep(60)
                continue

            df = add_rsi(df)
            signal = generate_signal(df)

            if signal:
                msg = f"📊 SIGNAL: {signal}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)


asyncio.run(main())
