import os
import asyncio
import requests
import pandas as pd
from datetime import datetime, timedelta
from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ✅ 5 COINS (CoinGecko IDs)
PAIRS = ["bitcoin", "ethereum", "binancecoin", "cardano", "ripple"]

# ✅ LAST SIGNAL STORE (10 min logic)
last_signals = {}

# ✅ DATA FETCH (CoinGecko - NO BLOCK)
def get_price(symbol):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": symbol, "vs_currencies": "usd"}

        res = requests.get(url, params=params)

        if res.status_code != 200:
            print("API Error:", res.status_code)
            return None

        data = res.json()

        if symbol not in data:
            return None

        return data[symbol]["usd"]

    except Exception as e:
        print("API Error:", e)
        return None


# ✅ FAKE RSI (PRICE BASED SIMPLE LOGIC)
def generate_signal(price_list):
    if len(price_list) < 5:
        return None

    if price_list[-1] > price_list[-2] > price_list[-3]:
        return "BUY"
    elif price_list[-1] < price_list[-2] < price_list[-3]:
        return "SELL"
    else:
        return None


# ✅ TIME WINDOW (1 MIN)
def get_time_window():
    now = datetime.utcnow()
    start = now.strftime("%H:%M")
    end = (now + timedelta(minutes=1)).strftime("%H:%M")
    return f"{start}-{end}"


# ✅ PRICE STORAGE
price_history = {pair: [] for pair in PAIRS}


# ✅ MAIN LOOP
async def main():
    print("Bot started...")

    while True:
        try:
            for pair in PAIRS:
                price = get_price(pair)

                if price is None:
                    continue

                price_history[pair].append(price)

                # last 20 prices hi rakho
                if len(price_history[pair]) > 20:
                    price_history[pair].pop(0)

                signal = generate_signal(price_history[pair])

                # ✅ 10 MIN ANTI-SPAM
                now = datetime.utcnow()
                if pair in last_signals:
                    last_time = last_signals[pair]
                    if (now - last_time).seconds < 600:
                        continue

                if signal:
                    time_window = get_time_window()

                    msg = f"""📊 SIGNAL: {signal}
PAIR: {pair.upper()}
TIME: {time_window}
TF: 1 MIN"""

                    await bot.send_message(chat_id=CHAT_ID, text=msg)

                    last_signals[pair] = now

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(10)


# ✅ RUN FIX
if __name__ == "__main__":
    asyncio.run(main())
