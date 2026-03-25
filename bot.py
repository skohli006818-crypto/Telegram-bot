import logging
import pytz
import yfinance as yf
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import asyncio

# 🔑 TOKEN & CHAT ID
TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
CHAT_ID = "7606599262"

# 📊 Pairs
pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]

# 🪵 Logging
logging.basicConfig(level=logging.INFO)

# 🇮🇳 Timezone
india = pytz.timezone("Asia/Kolkata")


# 🔥 SIGNAL LOGIC (SNIPER)
def get_signal():
    now = datetime.now(india)

    entry_time = (now + timedelta(minutes=3)).strftime("%H:%M")
    exit_time = (now + timedelta(minutes=4)).strftime("%H:%M")

    for pair in pairs:
        try:
            data = yf.download(pair, period="1d", interval="1m")

            if data.empty:
                continue

            data = data.tz_localize('UTC').tz_convert(india)

            close = data['Close']
            open_ = data['Open']
            high = data['High']
            low = data['Low']

            ema = EMAIndicator(close, window=50).ema_indicator()
            rsi = RSIIndicator(close, window=14).rsi()

            last_close = close.iloc[-1]
            last_open = open_.iloc[-1]
            last_ema = ema.iloc[-1]
            last_rsi = rsi.iloc[-1]

            support = low.tail(20).min()
            resistance = high.tail(20).max()

            bullish = last_close > last_open
            bearish = last_close < last_open

            near_support = abs(last_close - support) < (0.001 * last_close)
            near_resistance = abs(last_close - resistance) < (0.001 * last_close)

            # BUY
            if last_close > last_ema and last_rsi < 35 and bullish and near_support:
                return f"""
🚨 SIGNAL ALERT (3 MIN BEFORE)

Pair: {pair.replace('=X','')}
Direction: BUY 🟢
Entry Time: {entry_time} IST
"""

            # SELL
            if last_close < last_ema and last_rsi > 65 and bearish and near_resistance:
                return f"""
🚨 SIGNAL ALERT (3 MIN BEFORE)

Pair: {pair.replace('=X','')}
Direction: SELL 🔴
Entry Time: {entry_time} IST
"""

        except:
            continue

    return None


# 🔥 FINAL SIGNAL MESSAGE
def final_signal(alert_msg):
    now = datetime.now(india)
    exit_time = (now + timedelta(minutes=4)).strftime("%H:%M")

    return alert_msg + f"""
🚀 ENTRY NOW

⏳ Exit Time: {exit_time} IST

⚡ Strategy: RSI + EMA + S/R + Candle Confirm
"""


# 🤖 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 TRADING EXPERT GHOST ☠️\n\n"
        "⚡ Auto + Manual Signals Active\n"
        "📊 Strategy: RSI + EMA + S/R\n"
        "🇮🇳 Indian Time Based\n"
    )


# 📩 MANUAL SIGNAL
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sig = get_signal()
    if sig:
        await update.message.reply_text(sig)
        await asyncio.sleep(180)
        await update.message.reply_text(final_signal(sig))
    else:
        await update.message.reply_text("❌ No signal right now")


# 🔁 AUTO SIGNAL LOOP
async def auto_signal(app):
    while True:
        sig = get_signal()
        if sig:
            await app.bot.send_message(chat_id=CHAT_ID, text=sig)
            await asyncio.sleep(180)
            await app.bot.send_message(chat_id=CHAT_ID, text=final_signal(sig))

        await asyncio.sleep(60)  # check every 1 min


# 🚀 MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # 🔁 background task
    asyncio.create_task(auto_signal(app))

    print("Bot running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        asyncio.new_event_loop().run_until_complete(main())
