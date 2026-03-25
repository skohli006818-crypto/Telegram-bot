import logging
import datetime
import pytz
import yfinance as yf
import pandas as pd

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== CONFIG =====
TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

logging.basicConfig(level=logging.INFO)

# ===== TIME =====
ist = pytz.timezone("Asia/Kolkata")

# ===== DATA =====
def get_data():
    df = yf.download("EURUSD=X", interval="1m", period="1d")
    df.dropna(inplace=True)
    return df

# ===== SIGNAL LOGIC =====
def get_signal(symbol):
    df = yf.download(symbol, period="1d", interval="1m")
    df.dropna(inplace=True)

    df['EMA'] = df['Close'].ewm(span=20).mean()

    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]
    prev = df.iloc[-2]

    price = float(last['Close'])
    ema = float(last['EMA'])
    rsi = float(last['RSI'])

    prev_open = float(prev['Open'])
    prev_close = float(prev['Close'])

    buy_score = 0
    sell_score = 0

    if price > ema:
        buy_score += 1
    else:
        sell_score += 1

    if rsi < 45:
        buy_score += 1
    elif rsi > 55:
        sell_score += 1

    if prev_close > prev_open:
        buy_score += 1
    elif prev_close < prev_open:
        sell_score += 1

    if buy_score >= 2:
        return "BUY"
    elif sell_score >= 2:
        return "SELL"
    else:
        return None

# ===== FORMAT =====
def format_signal(sig):
    now = datetime.datetime.now(ist)

    entry = now + datetime.timedelta(minutes=3)
    exit_time = entry + datetime.timedelta(minutes=1)

    return f"""
🔥 TRADING EXPERT GHOST ☠️

📊 Pair: EUR/USD
⏱ Timeframe: 1 Min

🚀 Signal: {sig}

⏰ Entry: {entry.strftime('%H:%M:%S')} IST
⏳ Exit: {exit_time.strftime('%H:%M:%S')} IST

⚡ Strategy:
RSI + EMA + Candle Confirm
"""

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to PRO SIGNAL BOT\n\nType /signal to get signal"
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pairs = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X"
    }

    msg = "🔥 PRO SIGNAL\n\n"
    found = False

    for name, symbol in pairs.items():
        sig = get_signal(symbol)

        if sig:
            found = True
            msg += f"{name} → {sig}\n"

    if not found:
        msg += "❌ No strong signal"

    await update.message.reply_text(msg)

# ===== MAIN =====
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🔥 PRO BOT RUNNING...")
    app.run_polling()

# ===== RUN =====
if __name__ == "__main__":
    main()
