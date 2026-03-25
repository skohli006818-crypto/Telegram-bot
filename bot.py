import asyncio
import random
from datetime import datetime, timedelta
import pytz
import yfinance as yf
import pandas as pd

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
CHAT_ID = "7606599262"

# ================= INDIA TIME =================
def get_ist_time():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)

# ================= FETCH DATA =================
def get_data():
    data = yf.download(tickers="EURUSD=X", interval="1m", period="1d")
    return data

# ================= STRATEGY =================
def get_signal():
    df = get_data()

    if df is None or len(df) < 50:
        return None

    # EMA
    df['EMA'] = df['Close'].ewm(span=20).mean()

    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]

    price = last['Close']
    ema = last['EMA']
    rsi = last['RSI']

    # Support / Resistance
    support = df['Low'].rolling(20).min().iloc[-1]
    resistance = df['High'].rolling(20).max().iloc[-1]

    # Candle confirm
    prev = df.iloc[-2]

    signal = None

    # BUY
    if price > ema and rsi < 35 and prev['Close'] < prev['Open']:
        signal = "BUY"

    # SELL
    elif price < ema and rsi > 65 and prev['Close'] > prev['Open']:
        signal = "SELL"

    if not signal:
        return None

    return {
        "signal": signal,
        "price": round(price, 5),
        "support": round(support, 5),
        "resistance": round(resistance, 5)
    }

# ================= FORMAT =================
def format_signal(sig):
    now = get_ist_time()
    entry_time = now + timedelta(minutes=3)
    exit_time = entry_time + timedelta(minutes=1)

    return f"""
🚀 TRADING EXPERT GHOST ☠️

📊 Signal: {sig['signal']}
💰 Price: {sig['price']}

⏰ Entry: {entry_time.strftime('%H:%M:%S')} IST
⏳ Exit: {exit_time.strftime('%H:%M:%S')} IST

📉 Support: {sig['support']}
📈 Resistance: {sig['resistance']}

⚡ Strategy:
RSI + EMA + Candle Confirm
"""

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot Started - Pro Signals ON")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sig = get_signal()
    if sig:
        await update.message.reply_text(format_signal(sig))
    else:
        await update.message.reply_text("❌ No Signal Now")

# ================= AUTO LOOP =================
async def auto_loop(app):
    while True:
        sig = get_signal()
        if sig:
            await app.bot.send_message(
                chat_id=CHAT_ID,
                text="⚠️ Signal in 3 minutes..."
            )

            await asyncio.sleep(180)

            await app.bot.send_message(
                chat_id=CHAT_ID,
                text=format_signal(sig)
            )

        await asyncio.sleep(300)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🔥 PRO BOT RUNNING...")

    async def run():
        asyncio.create_task(auto_loop(app))
        await app.run_polling()

    asyncio.run(run())

if __name__ == "__main__":
    main()
