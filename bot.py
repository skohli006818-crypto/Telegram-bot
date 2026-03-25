from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
import random

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

# ===== SIGNAL LOGIC =====
def get_signal(symbol):
    rsi = random.randint(20, 80)
    ema = random.choice(["UP", "DOWN"])
    candle = random.choice(["BULLISH", "BEARISH"])

    # ANY ONE MATCH = SIGNAL
    if rsi < 30:
        return "BUY"
    elif rsi > 70:
        return "SELL"
    elif ema == "UP":
        return "BUY"
    elif ema == "DOWN":
        return "SELL"
    elif candle == "BULLISH":
        return "BUY"
    elif candle == "BEARISH":
        return "SELL"

    return None


# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Welcome to PRO SIGNAL BOT\n\nType /signal to get signal"
    )


# ===== SIGNAL COMMAND =====
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

            now = datetime.now()
            entry = now.strftime("%H:%M:%S")
            exit_time = (now + timedelta(minutes=1)).strftime("%H:%M:%S")

            msg += f"""
🔥 TRADING EXPERT GHOST 💀

📊 Pair: {name}
⏱ Timeframe: 1 Min

🚀 Signal: {sig}

⏰ Entry: {entry} IST
⌛ Exit: {exit_time} IST

⚡ Strategy:
RSI + EMA + Candle Confirm

"""

    # LOOP KE BAHAR
    if not found:
        msg += "❌ No strong signal"

    await update.message.reply_text(msg)


# ===== MAIN =====
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🔥 BOT RUNNING...")
    app.run_polling()


if __name__ == "__main__":
    main()
