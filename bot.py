import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

def generate_signal():
    pair = random.choice(PAIRS)
    direction = random.choice(["BUY", "SELL"])

    now = datetime.now()
    start = now.strftime("%H:%M")
    end = (now + timedelta(minutes=1)).strftime("%H:%M")

    return f"""📊 SIGNAL ALERT

📈 Pair: {pair}
📊 Signal: {direction}
⏰ Time: {start} - {end} (1 MIN)

🔥 STRONG SIGNAL
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Start command received")   # 👈 debug
    await update.message.reply_text("Bot working ✅\n\n" + generate_signal())

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Signal command received")  # 👈 debug
    await update.message.reply_text(generate_signal())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot running...")

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
