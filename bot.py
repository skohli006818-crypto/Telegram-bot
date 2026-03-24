import os
import asyncio
import requests
import pandas as pd
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# 5 Pairs (crypto ko forex naam de rahe hain style ke liye)
PAIRS = {
    "EUR/USD": "bitcoin",
    "GBP/USD": "ethereum",
    "USD/JPY": "litecoin",
    "AUD/USD": "ripple",
    "USD/CAD": "cardano"
}

bot = Bot(token=TOKEN)

last_signals = []  # store last 10 min signals


# ================= API =================
def get_data(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1"
        res = requests.get(url)

        if res.status_code != 200:
            return None

        data = res.json().get("prices", [])
        if not data:
            return None

        df = pd.DataFrame(data, columns=["time", "price"])
        df["price"] = df["price"].astype(float)

        return df

    except:
        return None


# ================= RSI =================
def add_rsi(df):
    delta = df["price"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()

    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


# ================= SIGNAL =================
def generate_signal(df):
    if df is None or len(df) < 20:
        return None

    rsi = df["rsi"].iloc[-1]

    if rsi < 30:
        return "BUY"
    elif rsi > 70:
        return "SELL"
    return None


# ================= FORMAT =================
def format_signal(pair, signal):
    now = datetime.utcnow()
    start = now.strftime("%H:%M")
    end = (now + timedelta(minutes=1)).strftime("%H:%M")

    return f"""📊 SIGNAL: {signal}
PAIR: {pair}
TIME: {start} - {end}
FRAME: 1 MIN"""


# ================= LOOP =================
async def signal_loop(app):
    global last_signals

    while True:
        try:
            new_signals = []

            for pair, coin in PAIRS.items():
                df = get_data(coin)

                if df is None:
                    continue

                df = add_rsi(df)
                signal = generate_signal(df)

                if signal:
                    msg = format_signal(pair, signal)
                    new_signals.append(msg)

                    # send to all users (broadcast)
                    for user in app.bot_data.get("users", []):
                        await app.bot.send_message(chat_id=user, text=msg)

            # store last 10 min signals
            if new_signals:
                last_signals.extend(new_signals)

            # keep only last 10 min approx (10-20 signals)
            last_signals = last_signals[-20:]

            await asyncio.sleep(60)

        except Exception as e:
            print("Loop Error:", e)
            await asyncio.sleep(60)


# ================= COMMAND =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if "users" not in context.bot_data:
        context.bot_data["users"] = []

    if user_id not in context.bot_data["users"]:
        context.bot_data["users"].append(user_id)

    await update.message.reply_text("✅ Bot Started!\nUse /signal")


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not last_signals:
        await update.message.reply_text("❌ No recent signals")
        return

    # send latest signal
    await update.message.reply_text(last_signals[-1])


# ================= MAIN =================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # start loop
    asyncio.create_task(signal_loop(app))

    print("Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
