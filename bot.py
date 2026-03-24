import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pytz

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

# India Timezone
IST = pytz.timezone("Asia/Kolkata")

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

def generate_signal():
    pair = random.choice(pairs)
    signal = random.choice(["BUY", "SELL"])

    now = datetime.now(IST)

    # next 10 min ke andar random time
    future_time = now + timedelta(minutes=random.randint(1, 10))
    end_time = future_time + timedelta(minutes=1)

    time_range = f"{future_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

    return f"""📊 SIGNAL: {signal}
💱 PAIR: {pair}
⏱ TIMEFRAME: 1 MIN
🕐 ENTRY: {time_range} (IST)
🔥 STRENGTH: STRONG"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Active (IST Time)\nType /signal")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = []

    for _ in range(5):  # 5 pairs
        signals.append(generate_signal())

    response = "\n\n".join(signals)

    await update.message.reply_text(response)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")

app.run_polling()
