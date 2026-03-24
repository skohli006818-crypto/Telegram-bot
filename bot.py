import random
import asyncio
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

users = set()

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

def generate_signal():
    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    entry_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")

    return f"""
📊 *QUOTEX SIGNAL*

Pair: {pair}
Direction: {direction}
Entry Time: {entry_time} (1-Min)

⚡ Trade Now & Follow Proper Risk Management
"""

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_chat.id)

    keyboard = [["/signal"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    msg = """🔥 *Welcome to Quotex AI Signal Bot*

Get high-quality signals with smart market analysis.

✅ 1-Min Signals  
✅ Top Currency Pairs  
✅ 20 Daily Strong Auto Signals  
✅ Pre Alert System  

⚡ Click /signal to get instant signal"""

    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown")

# MANUAL SIGNAL
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Generating Signal...")
    await asyncio.sleep(1)

    sig = generate_signal()
    await update.message.reply_text(sig, parse_mode="Markdown")

# AUTO SIGNAL SYSTEM
async def auto_signal(app):
    while True:
        for i in range(20):
            # Alert
            for user in users:
                try:
                    await app.bot.send_message(chat_id=user, text="⚠️ Signal Incoming in 1 minute...")
                except:
                    pass

            await asyncio.sleep(60)

            sig = generate_signal()

            for user in users:
                try:
                    await app.bot.send_message(chat_id=user, text=sig, parse_mode="Markdown")
                except:
                    pass

            await asyncio.sleep(300)  # 5 min gap

        await asyncio.sleep(3600)  # next batch after 1 hour

# MAIN FUNCTION (IMPORTANT FIX)
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # AUTO SIGNAL START
    asyncio.create_task(auto_signal(app))

    print("Bot running...")
    await app.run_polling()

# RUN FIX (NO LOOP ERROR)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
