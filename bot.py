import os
import asyncio
import requests
import pandas as pd
from telegram import Bot

TOKEN = os.getenv("8719400693:AAFbw8e0jrunWL9pY10ZKQVUaFcNBATq-u8")
CHAT_ID = os.getenv("7606599262")

bot = Bot(token=TOKEN)

def get_data():
    url = "https://api.binance.com/api/v3/klines?symbol=EURUSDT&interval=1m&limit=50"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","trades","taker_base","taker_quote","ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

def add_rsi(df):
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def generate_signal(df):
    last_rsi = df["rsi"].iloc[-1]

    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return None

async def main():
    print("Bot started...")

    while True:
        try:
            df = get_data()
            df = add_rsi(df)

            signal = generate_signal(df)

            if signal:
                message = f"📊 SIGNAL: {signal}\nPAIR: EUR/USD\nTIME: 1 MIN"
                await bot.send_message(chat_id=CHAT_ID, text=message)

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
