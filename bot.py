import yfinance as yf
import pandas as pd
import pytz
import asyncio
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
CHAT_ID = "7606599262"

# ===== GET MARKET DATA =====
def get_data():
    data = yf.download(tickers="EURUSD=X", interval="1m", period="1d")
    return data

# ===== STRATEGY =====
def get_signal():
    df = get_data()
    if df.empty or len(df) < 60:
        return None

    df['EMA'] = df['Close'].ewm(span=50).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]

    # Support / Resistance
    support = df['Low'].rolling(20).min().iloc[-1]
    resistance = df['High'].rolling(20).max().iloc[-1]

    # Candle
    open_price = last['Open']
    close_price = last['Close']

    # ===== BUY =====
    if (last['RSI'] < 30 and
        close_price > last['EMA'] and
        close_price > open_price and
        close_price <= support * 1.02):

        return "CALL"

    # ===== SELL =====
    if (last['RSI'] > 70 and
        close_price < last['EMA'] and
        close_price < open_price and
        close_price >= resistance * 0.98):

        return "PUT"

    return None

# ===== TIME FORMAT (IST) =====
def get_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    entry = now + timedelta(minutes=3)
    exit_time = entry + timedelta(minutes=1)

    return entry.strftime("%H:%M"), exit_time.strftime("%H:%M")

# ===== FORMAT MESSAGE =====
def format_signal(sig):
    entry, exit_time = get_time()
    return f"""🔥 STRONG SIGNAL

PAIR: EUR/USD
TIMEFRAME: 1 MIN

DIRECTION: {sig}

ENTRY TIME: {entry} (IST)
EXIT TIME: {exit_time} (IST)

⚠️ Use Proper Risk Management"""

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 PRO BOT STARTED\nType /signal")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sig = get_signal()
    if sig:
        await update.message.reply_text(format_signal(sig))
        async def auto_loop(app):
    while True:
        sig = get_signal()
        if sig:
            await app.bot.send_message(chat_id=CHAT_ID, text="⚠️ Signal in 3 min...")
            await asyncio.sleep(180)
            await app.bot.send_message(chat_id=CHAT_ID, text=format_signal(sig))

        await asyncio.sleep(300)
    else:
        await update.message.reply_text("❌ No strong signal right now")

# ===== AUTO SIGNAL LOOP =====
    sig = get_signal()
    if sig:
        # Alert before 3 min
        await context.bot.send_message(chat_id=CHAT_ID, text="⚠️ Signal coming in 3 minutes...")

        await asyncio.sleep(180)

        await context.bot.send_message(chat_id=CHAT_ID, text=format_signal(sig))

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🔥 PRO BOT RUNNING...")

    async def run():
        asyncio.create_task(auto_loop(app))
        await app.run_polling()

    asyncio.run(run())

if __name__ == "__main__":
    main()
