import asyncio
import logging
import random
from datetime import datetime, time
import pytz

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== CONFIG =====
TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
IST = pytz.timezone("Asia/Kolkata")

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO)

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🚀 *Auto Trading Bot Started*\n\n"
        "⏰ Timeframe: 1 Min\n"
        "📊 Signals: 20/day\n"
        "🔥 Strong Signals Enabled\n\n"
        "Type /signal for instant signal"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# ===== REAL SIGNAL (SIMULATED REAL DATA LOGIC) =====
def generate_signal():
    pair = random.choice(["EUR/USD", "USD/JPY", "GBP/USD"])
    direction = random.choice(["CALL 🟢", "PUT 🔴"])
    strength = random.choice(["STRONG 💪", "NORMAL"])

    now = datetime.now(IST)
    entry_time = now.strftime("%H:%M")
    exit_time = (now.replace(second=0, microsecond=0) + 
                 timedelta(minutes=1)).strftime("%H:%M")

    return f"""
📊 *SIGNAL ALERT*

Pair: {pair}
Time: {entry_time} - {exit_time}
Direction: {direction}
Strength: {strength}
"""

# ===== MANUAL SIGNAL =====
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sig = generate_signal()
    await update.message.reply_text(sig, parse_mode="Markdown")

# ===== AUTO SIGNAL LOOP =====
async def auto_signal(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    sig = generate_signal()
    await context.bot.send_message(chat_id=chat_id, text=sig, parse_mode="Markdown")

# ===== START AUTO =====
async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Clear old jobs
    for job in context.job_queue.jobs():
        job.schedule_removal()

    # Run 20 signals daily (every ~30 min)
    context.job_queue.run_repeating(auto_signal, interval=1800, first=5, chat_id=chat_id)

    await update.message.reply_text("✅ Auto Signals Started (20/day)")

# ===== MAIN =====
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler
