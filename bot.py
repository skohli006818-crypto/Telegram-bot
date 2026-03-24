import os
import asyncio
import requests
import pandas as pd
from telegram import Bot

# ENV variables
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# 📊 Get Data from Binance
def get_data():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=EURUSDT&interval=1m&limit=100"
        data = requests.get(url).json()

        df = pd.DataFrame(data, columns=[
            "time","open","high","low","close","volume",
            "close_time","qav","trades","tbbav","tbqav","ignore"
        ])

        df["close"] = df["close"].astype(float)

        return df

    except Exception as e:
        print("Data Error:", e)
        return None


# 📉 RSI Indicator
def add_rsi(df):
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


# 📢 Signal Generator
def generate_signal(df):
    if df is None or len(df) < 20:
        return None

    last_rsi = df["rsi"].iloc[-1]

    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return None


# 🤖 Main Bot Loop
async def main():
    print("Bot started...")

    while True:
        try:
            df = get_data()

            if df is None or df.empty:
                print("No data")
                await asyncio.sleep(60)
                continue

            df = add_rsi(df)
            signal = generate_signal(df)

            if signal:
                message = f"📊 SIGNAL: {signal}\nPAIR: EUR/USD\nTIME: 1 MIN"
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print("Signal sent:", signal)

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)


# ▶️ Run Bot
if __name__ == "__main__":
    asyncio.run(main())
