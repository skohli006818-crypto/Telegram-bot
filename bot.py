import asyncio
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"

pairs = ["EUR/USD", "USD/JPY", "GBP/USD", "AUD/USD", "EUR/JPY"]
users = set()
auto_signals_sent = 0

# 🇮🇳 Indian Time
def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

# 🔥 Signal Generator
def generate_signal():
    pair = random.choice(pairs)
    signal = random.choice(["BUY", "SELL"])
    now = get_ist_time()
    start = now.strftime("%H:%M")
    end = (now + timedelta(minutes=1)).strftime("%H:%M")

    return f"""
🔥 STRONG SIGNAL 🔥
PAIR: {pair}
SIGNAL: {signal}
TIME: {start} - {end}
TIMEFRAME: 1 MIN
"""

# 🧾 Description
WELCOME_TEXT = """🔥 Welcome to Quotex AI Signal Bot 🔥

Get access to high-quality trading signals powered by smart market analysis and advanced strategy.

✅ 1-Minute Accurate Signals
✅ Top 5 Major Currency Pairs
✅ Real-Time Market Analysis
✅ Instant Signals on Demand
✅ 20 Daily Strong Auto Signals
✅ Pre-Signal Alerts (1–2 min before)

Our system continuously scans the market and delivers high-probability signals to help you take better trading decisions.

📊 Signals include:
Pair (EUR/USD, GBP/USD, etc.)
Direction (BUY / SELL)
Exact Entry Time (1-Min Window)
Strong Accuracy Setup

⚡ Click below to get signal instantly.
"""

# 👤 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)

    keyboard = [
        [InlineKeyboardButton("🚀 Get Signal", callback_data="get_signal")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# 📩 Manual Signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = generate_signal()
    await update.message.reply_text(msg)

# 🎯 Button Click
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_signal":
        msg = generate_signal()
        await query.message.reply_text(msg)

# 🔔 Auto Signal System
async def auto_signal_loop(app):
    global auto_signals_sent

    while True:
        if auto_signals_sent < 20:

            wait_time = random.randint(600, 1200)  # 10-20 min gap
            await asyncio.sleep(wait_time)

            # 🔔 Alert
            for user in users:
                try:
                    await app.bot.send_message(
                        chat_id=user,
                        text="⚠️ Strong Signal Incoming in 1-2 Minutes!"
                    )
                except:
                    pass

            await asyncio.sleep(90)

            # 📊 Signal send
            msg = generate_signal()
            for user in users:
                try:
                    await app.bot.send_message(chat_id=user, text=msg)
                except:
                    pass

            auto_signals_sent += 1
            print(f"Auto Signal Sent: {auto_signals_sent}")

        else:
            print("✅ Daily limit reached (20 signals)")
            await asyncio.sleep(3600)

# ⏳ Delay Start Fix
async def delayed_auto_start(app):
    await asyncio.sleep(60)  # 1 min delay
    await auto_signal_loop(app)

# 🚀 MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")

    asyncio.create_task(delayed_auto_start(app))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
