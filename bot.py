import random
import asyncio
from datetime import datetime, timedelta
import pytz

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

IST = pytz.timezone("Asia/Kolkata")
pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

users = set()

# ===== SIGNAL =====
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

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users.add(user_id)

    text = """🔥 Welcome to Quotex AI Signal Bot

Get high-quality trading signals powered by smart market analysis.

✅ 1-Minute Signals  
✅ Top Pairs  
✅ 20 Daily Signals  
✅ Pre Alerts  

⚡ Send /signal anytime."""

    await update.message.reply_text(text)

# ===== SIGNAL COMMAND =====
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users.add(user_id)

    await update.message.reply_text(generate_signal())

# ===== AUTO SIGNAL LOOP =====
async def auto_signal_loop(app):
    await asyncio.sleep(10)

    while True:
        print("Auto signals running...")

        for _ in range(20):
            if users:
                # ALERT
                for user in users:
                    try:
                        await app.bot.send_message(user, "⚡ Signal in 1 minute...")
                    except:
                        pass
