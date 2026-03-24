import random
import time
from telegram.ext import Updater, CommandHandler

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

users = set()
pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

def generate_signal():
    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    return f"""
📊 SIGNAL

Pair: {pair}
Direction: {direction}
Time: 1 Minute ⏱

🔥 Strong Setup
"""

def start(update, context):
    users.add(update.message.chat_id)
    update.message.reply_text("🔥 Bot started! Use /signal")

def signal(update, context):
    update.message.reply_text(generate_signal())

def auto_signal(context):
    for user in users:
        context.bot.send_message(chat_id=user, text="⚠️ Signal in 1 min...")
        time.sleep(60)
        context.bot.send_message(chat_id=user, text=generate_signal())

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))

    # auto signal every 30 min
    updater.job_queue.run_repeating(auto_signal, interval=1800, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
