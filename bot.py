import os
import asyncio
import requests
import pandas as pd
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ================= DATA =================
def get_data():
    try:
        url = "https://api.bybit.com/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": "BTCUSDT",
            "interval": "1",
            "limit": 100
        }

        res = requests.get(url, params=params, timeout=10).json()

        if "result" not in res:
            print("No data from API")
            return None

        data = res["result"]["list"]

        if not data:
            print("Empty data")
            return None

        df = pd.DataFrame(data)

        df = df.iloc[:, :6]
        df.columns = ["time", "open", "high", "low", "close", "volume"]

        df["close"] = df["close"].astype(float)

        return df[::-1]

    except Exception as e:
        print("API Error:", e)
        return None

# ================= RSI =================
def add_rsi(df):
    delta = df["close"].diff()

    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()

    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df

# ================= SIGNAL =================
def generate_signal(df):
    if df is None or len(df) < 20:
        print("Not enough data")
        return None

    last_rsi = df["rsi"].iloc[-1]

    if last_rsi < 30:
        return "BUY"
    elif last_rsi > 70:
        return "SELL"
    else:
        return None

# ================= MAIN =================
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
                message = f"🔥 SIGNAL: {signal}"
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print("Signal sent:", signal)
            else:
                print("No signal")

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
