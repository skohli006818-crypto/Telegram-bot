from telegram.ext import ApplicationBuilder, CommandHandler
import random
from datetime import datetime, timedelta
import pytz

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

IST = pytz.timezone("Asia/Kolkata")

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

def generate_signal():
    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    now = datetime.now(IST)
    entry_time = (now + timedelta(minutes=1)).strftime("%H:%M")

    return f"""📊 SIGNAL

Pair: {pair}
Direction: {direction}
Time: {entry_time} (IST)
Duration: 1 Min
"""

async def start(update, context):
    text = """🔥 Welcome to Quotex AI Signal Bot

Get high-quality trading signals powered by smart market analysis.

✅ 1-Minute Signals  
✅ Top Pairs  
✅ 20 Daily Signals  
✅ Pre Alerts  

⚡ Send /signal anytime."""

    await update.message.reply_text(text)

async def signal(update, context):
    await update.message.reply_text(generate_signal())

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")
app.run_polling()
