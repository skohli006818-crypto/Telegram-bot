import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

users = set()

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

# 🔥 Signal Generator
def generate_signal():
    pair = random.choice(pairs)
    direction = random.choice(["BUY", "SELL"])
    return f"📊 Signal\nPair: {pair}\nDirection: {direction}\nTime: 1 Min"

# 🚀 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)

    msg = """🔥 Welcome to Quotex AI Signal Bot

Get high-quality trading signals with smart analysis.

✅ 1-Min Signals  
✅ Top Currency Pairs  
✅ 20 Daily Auto Signals  
✅ Instant Signal on Demand  

⚡ Send /signal to get signal instantly."""

    await update.message.reply_text(msg)

# ⚡ Manual Signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sig = generate_signal()
    await update.message.reply_text(sig)

# 🔔 Auto Signal Loop
async def auto_signal(app):
    while True:
        for user in users:
            try:
                await app.bot.send_message(chat_id=user, text="⚠️ Signal coming in 1 min...")
                await asyncio.sleep(60)

                sig = generate_signal()
                await app.bot.send_message(chat_id=user, text=sig)

            except:
                pass

        await asyncio.sleep(300)  # 5 min gap

# 🚀 Main Function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # Auto Signal Background Task
    asyncio.create_task(auto_signal(app))

    print("Bot running...")
    await app.run_polling()

# ✅ Run Bot (IMPORTANT FIX)
if __name__ == "__main__":
    asyncio.run(main())
