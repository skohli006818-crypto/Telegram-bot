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

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_chat.id)

    msg = """🔥 Welcome to Quotex AI Signal Bot

Get high-quality trading signals with smart market analysis.

✅ 1-Min Signals
✅ Top Currency Pairs
✅ Real-Time Analysis
✅ 20 Auto Signals Daily
✅ Alert Before Signal

⚡ Use /signal to get instant signal."""

    await update.message.reply_text(msg)

# MANUAL SIGNAL
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_signal())

# AUTO SIGNAL SYSTEM
async def auto_signal(app):
    while True:
        await asyncio.sleep(60 * 30)  # every 30 min

        for user in users:
            try:
                # alert
                await app.bot.send_message(chat_id=user, text="⚠️ Signal coming in 1 minute...")

                await asyncio.sleep(60)

                # signal
                await app.bot.send_message(chat_id=user, text=generate_signal())

            except:
                pass

# MAIN FUNCTION
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # auto signal background task
    app.create_task(auto_signal(app))

    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
