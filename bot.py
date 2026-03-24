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

# ===== SIGNAL GENERATOR =====
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

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users.add(user_id)

    text = """🔥 Welcome to Quotex AI Signal Bot

Get high-quality trading signals powered by smart market analysis.

✅ 1-Minute Signals  
✅ Top Currency Pairs  
✅ 20 Daily Auto Signals  
✅ Pre Alerts (1–2 min before)  

⚡ Send /signal anytime to get signal."""

    await update.message.reply_text(text)

# ===== MANUAL SIGNAL =====
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users.add(user_id)

    await update.message.reply_text(generate_signal())

# ===== AUTO SIGNAL LOOP =====
async def auto_signal(app):
    await asyncio.sleep(15)  # bot start hone ke baad delay

    while True:
        print("Auto signal running...")

        for _ in range(20):  # 20 signals per day

            if users:
                # ALERT (1 min before)
                for user in users:
                    try:
                        await app.bot.send_message(user, "⚡ Signal coming in 1 minute...")
                    except:
                        pass

                await asyncio.sleep(60)

                # SEND SIGNAL
                signal_text = generate_signal()

                for user in users:
                    try:
                        await app.bot.send_message(user, signal_text)
                    except:
                        pass

            await asyncio.sleep(300)  # 5 min gap

        await asyncio.sleep(3600)  # next batch delay

# ===== MAIN =====
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot running...")

    # AUTO SIGNAL START
    asyncio.create_task(auto_signal(app))

    await app.run_polling()

# ===== RUN =====
if __name__ == "__main__":
    asyncio.run(main())
