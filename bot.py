import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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

🔥 Strong Setup | High Probability
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_chat.id)

    msg = """🔥 Welcome to Quotex AI Signal Bot

Get smart & high-quality signals.

✅ 1-Min Signals
✅ Auto Signals Daily
✅ Real-Time Analysis

⚡ Use /signal to get signal."""

    await update.message.reply_text(msg)

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_signal())

async def auto_signal(app):
    await asyncio.sleep(10)  # startup delay

    while True:
        for user in users:
            try:
                await app.bot.send_message(chat_id=user, text="⚠️ Signal in 1 min...")
                await asyncio.sleep(60)
                await app.bot.send_message(chat_id=user, text=generate_signal())
            except:
                pass

        await asyncio.sleep(1800)  # 30 min

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # background task
    app.post_init = lambda app: app.create_task(auto_signal(app))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
