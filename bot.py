import logging
import random
from datetime import datetime, timedelta
import pytz

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ====== TOKEN ======
TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)

# ====== SMART SIGNAL FUNCTION ======
def get_signal(symbol):
    # Demo logic (later real API laga sakte hai)
    rsi = random.randint(20, 80)
    ema = random.choice(["UP", "DOWN"])
    candle = random.choice(["BULLISH", "BEARISH"])

    score = 0
    signal = None

    # RSI (strong)
    if rsi < 30:
        score += 2
        signal = "BUY"
    elif rsi > 70:
        score += 2
        signal = "SELL"

    # EMA
    if ema == "UP":
        score += 1
        if not signal:
            signal = "BUY"
    elif ema == "DOWN":
        score += 1
        if not signal:
            signal = "SELL"

    # Candle
    if candle == "BULLISH":
        score += 1
        if not signal:
            signal = "BUY"
    elif candle == "BEARISH":
        score += 1
        if not signal:
            signal = "SELL"

    return signal, score


# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to PRO SIGNAL BOT\n\nType /signal to get best signal"
    )


# ====== SIGNAL COMMAND ======
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pairs = {
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X",
        "AUD/USD": "AUDUSD=X"
    }

    best_pair = None
    best_signal = None
    best_score = 0

    # 👉 Smart selection
    for name, symbol in pairs.items():
        sig, score = get_signal(symbol)

        if score > best_score:
            best_score = score
            best_pair = name
            best_signal = sig

    if not best_signal:
        await update.message.reply_text("❌ No strong signal")
        return

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    entry_time = now + timedelta(minutes=2)
    exit_time = entry_time + timedelta(minutes=1)

    entry = entry_time.strftime("%H:%M:%S")
    exit_time = exit_time.strftime("%H:%M:%S")

    msg = f"""
🔥 PRO SIGNAL

🔥 TRADING EXPERT GHOST 💀

📊 Pair: {best_pair}
⏱ Timeframe: 1 Min

🚀 Signal: {best_signal}

🔥 Strength: {best_score}/4

⏰ Entry: {entry} IST
⌛ Exit: {exit_time} IST

⚡ Strategy:
RSI + EMA + Candle Confirm
"""

    await update.message.reply_text(msg)


# ====== MAIN ======
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🔥 BOT RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()
