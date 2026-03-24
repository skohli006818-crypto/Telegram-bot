import requests
import pandas as pd
import ta
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8719400693:AAFbw8e0jrunWL9pY10ZKQVUaFcNBATq-u8")

PAIRS = {
    "EUR/USD": "EURUSDT",
    "GBP/USD": "GBPUSDT",
    "USD/JPY": "USDJPY"
}

last_signals = {}

def get_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df = df.iloc[:, :6]
    df.columns = ["time","open","high","low","close","volume"]
    df["close"] = df["close"].astype(float)
    return df

def add_indicators(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["ma_fast"] = df["close"].rolling(10).mean()
    df["ma_slow"] = df["close"].rolling(20).mean()
    return df

def generate_signal(df):
    rsi = df["rsi"].iloc[-1]
    fast = df["ma_fast"].iloc[-1]
    slow = df["ma_slow"].iloc[-1]

    if rsi < 30 and fast > slow:
        return "BUY"
    elif rsi > 70 and fast < slow:
        return "SELL"
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.application.chat_data[chat_id] = True
    await update.message.reply_text("Bot started ✅\nUse /signal")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 LIVE SIGNALS:\n\n"
    for pair_name, symbol in PAIRS.items():
        df = get_data(symbol)
        df = add_indicators(df)
        sig = generate_signal(df) or "NO SIGNAL"
        msg += f"{pair_name} → {sig}\n"
    await update.message.reply_text(msg)

async def auto_signal(app):
    while True:
        try:
            for pair_name, symbol in PAIRS.items():
                df = get_data(symbol)
                df = add_indicators(df)
                signal = generate_signal(df)

                if signal and last_signals.get(pair_name) != signal:
                    message = f"📊 AUTO SIGNAL\nPAIR: {pair_name}\nSIGNAL: {signal}"

                    for chat_id in app.chat_data:
                        await app.bot.send_message(chat_id=chat_id, text=message)

                    last_signals[pair_name] = signal

            await asyncio.sleep(60)

        except Exception as e:
            print(e)
            await asyncio.sleep(60)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    asyncio.create_task(auto_signal(app))

    print("Bot running...")

    await app.run_polling()

asyncio.run(main())
