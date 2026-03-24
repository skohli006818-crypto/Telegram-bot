import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pytz

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

IST = pytz.timezone("Asia/Kolkata")

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

# user cooldown storage
user_last_used = {}

COOLDOWN_SECONDS = 120  # 2 minutes

def generate_signal():
    pair = random.choice(pairs)
    signal = random.choice(["BUY", "SELL"])

    now = datetime.now(IST)

    future_time = now + timedelta(minutes=random.randint(1, 10))
    end_time = future_time + timedelta(minutes=1)

    time_range = f"{future_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

    return f"""📊 SIGNAL: {signal}
💱 PAIR: {pair}
⏱ TIMEFRAME: 1 MIN
🕐 ENTRY: {time_range} (IST)
🔥 STRENGTH: STRONG"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Ready\nUse /signal")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.now()

    # cooldown check
    if user_id in user_last_used:
        diff = (now - user_last_used[user_id]).total_seconds()
        if diff < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - diff)
            await update.message.reply_text(
                f"⏳ Wait {remaining} sec before next signal"
            )
            return

    # update last used time
    user_last_used[user_id] = now

    # send signal
    signal_msg = generate_signal()
    await update.message.reply_text(signal_msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")

app.run_polling()
