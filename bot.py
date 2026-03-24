from telegram.ext import Updater, CommandHandler
import random
from datetime import datetime, timedelta
import pytz

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

users = set()
daily_count = 0

pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "USD/CAD"]

# ===== GENERATE SIGNAL =====
def generate_signal():
    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)

    entry_time = (now + timedelta(minutes=3)).strftime("%H:%M")
    exit_time = (now + timedelta(minutes=4)).strftime("%H:%M")

    pair = random.choice(pairs)
    direction = random.choice(["BUY 🟢", "SELL 🔴"])

    return f"""
📊 STRONG SIGNAL

Pair: {pair}
Direction: {direction}

⏰ Entry: {entry_time} (IST)
⏳ Exit: {exit_time} (IST)

Timeframe: 1 Min ⏱
🔥 High Probability
"""

# ===== START =====
def start(update, context):
    users.add(update.message.chat_id)
    update.message.reply_text(
        "🔥 Auto Signal Bot Started\n\n"
        "📊 20 Signals Daily\n"
        "⏰ Entry Time Future Based (3 min)\n"
        "⚡ Auto + Manual Signals\n\n"
        "Use /signal"
    )

# ===== MANUAL SIGNAL =====
def signal(update, context):
    update.message.reply_text("⏳ Generating signal...")
    update.message.reply_text(generate_signal())

# ===== AUTO SIGNAL =====
def auto_signal(context):
    global daily_count

    india = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india)

    # reset daily
    if now.hour == 0 and now.minute == 0:
        daily_count = 0

    if daily_count >= 20:
        return

    # हर 30 min pe signal
    if now.minute % 30 == 0:
        for user in users:
            # ALERT (3 min before)
            context.bot.send_message(
                chat_id=user,
                text="⚠️ Strong Signal coming in 3 minutes..."
            )

        # wait 3 minutes
        import time
        time.sleep(180)

        # SEND SIGNAL
        for user in users:
            context.bot.send_message(chat_id=user, text=generate_signal())

        daily_count += 1

# ===== MAIN =====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))

    updater.job_queue.run_repeating(auto_signal, interval=60, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
