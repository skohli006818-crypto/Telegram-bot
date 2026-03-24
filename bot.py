import random
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pytz

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
CHAT_ID = "7606599262"

IST = pytz.timezone("Asia/Kolkata")

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD"]

# cooldown
user_last_used = {}
COOLDOWN_SECONDS = 60

# auto limit
AUTO_SIGNAL_LIMIT = 20
auto_signal_count = 0
last_reset_day = None


# 👤 manual signal
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.now()

    if user_id in user_last_used:
        diff = (now - user_last_used[user_id]).total_seconds()
        if diff < COOLDOWN_SECONDS:
            await update.message.reply_text(
                f"⏳ Wait {int(COOLDOWN_SECONDS - diff)} sec"
            )
            return

    user_last_used[user_id] = now

    pair = random.choice(pairs)
    signal_type = random.choice(["BUY", "SELL"])

    now_ist = datetime.now(IST)
    entry = now_ist + timedelta(minutes=1)
    end = entry + timedelta(minutes=1)

    msg = f"""📊 SIGNAL
💱 PAIR: {pair}
📈 TYPE: {signal_type}
⏱ TF: 1 MIN
🕐 ENTRY: {entry.strftime('%H:%M')} - {end.strftime('%H:%M')} (IST)
🔥 CONFIDENCE: HIGH"""

    await update.message.reply_text(msg)


# 🤖 AUTO SYSTEM (ALERT + SIGNAL)
async def auto_signals(app):
    global auto_signal_count, last_reset_day

    while True:
        try:
            now = datetime.now(IST)
            today = now.date()

            # reset daily
            if last_reset_day != today:
                auto_signal_count = 0
                last_reset_day = today

            if auto_signal_count < AUTO_SIGNAL_LIMIT:

                # entry time (2–5 min future)
                entry_time = now + timedelta(minutes=random.randint(2, 5))
                end_time = entry_time + timedelta(minutes=1)

                pair = random.choice(pairs)
                signal_type = random.choice(["BUY", "SELL"])

                # 🔔 ALERT MESSAGE
                alert_msg = f"""⚠️ Upcoming Signal
💱 PAIR: {pair}
⏳ Entry at {entry_time.strftime('%H:%M')} (IST)
Stay ready 📊"""

                await app.bot.send_message(chat_id=CHAT_ID, text=alert_msg)

                # ⏱ wait till entry time
                wait_seconds = (entry_time - datetime.now(IST)).total_seconds()
                if wait_seconds > 0:
                    await asyncio.sleep(wait_seconds)

                # 📊 FINAL SIGNAL
                signal_msg = f"""📊 STRONG SIGNAL
💱 PAIR: {pair}
📈 TYPE: {signal_type}
⏱ TF: 1 MIN
🕐 ENTRY: {entry_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} (IST)
🔥 CONFIDENCE: HIGH"""

                await app.bot.send_message(chat_id=CHAT_ID, text=signal_msg)

                auto_signal_count += 1
                print(f"Auto Signal {auto_signal_count}")

                await asyncio.sleep(120)  # gap between signals

            else:
                await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(10)


# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Active\nUse /signal anytime")


# 🚀 main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot running...")

    asyncio.create_task(auto_signals(app))

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
