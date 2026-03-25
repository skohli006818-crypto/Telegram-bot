import asyncio
import datetime
import pytz
import yfinance as yf
import pandas as pd

from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "8630040886:AAEqpx9TM0NRkhiWS8a6oB1AY71C5uiYce4"
CHAT_ID = "7606599262"

bot = Bot(token=TOKEN)

# ================= TIME =================
ist = pytz.timezone("Asia/Kolkata")

# ================= DATA =================
def get_data():
    df = yf.download(tickers="EURUSD=X", interval="1m", period="1d")
    df.dropna(inplace=True)
    return df

# ================= INDICATORS =================
def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_support_resistance(df):
    support = df['Low'].rolling(10).min().iloc[-1]
    resistance = df['High'].rolling(10).max().iloc[-1]
    return support, resistance

# ================= SIGNAL =================
def get_signal():
    df = get_data()

    df['EMA'] = df['Close'].ewm(span=20).mean()
    df['RSI'] = calculate_rsi(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    price = float(last['Close'])
    ema = float(last['EMA'])
    rsi = float(last['RSI'])

    prev_close = float(prev['Close'])
    prev_open = float(prev['Open'])

    support, resistance = get_support_resistance(df)

    signal = "NO SIGNAL"

    # ===== BUY =====
    if price > ema and rsi < 35 and prev_close > prev_open and price > support:
        signal = "BUY"

    # ===== SELL =====
    elif price < ema and rsi > 65 and prev_close < prev_open and price < resistance:
        signal = "SELL"

    return signal, price, support, resistance

# ================= MESSAGE =================
def format_signal():
    signal, price, support, resistance = get_signal()

    now = datetime.datetime.now(ist)
    entry_time = now + datetime.timedelta(minutes=3)
    exit_time = entry_time + datetime.timedelta(minutes=1)

    msg = f"""
🔥 PRO SIGNAL 🔥

Signal: {signal}
Pair: EUR/USD
Timeframe: 1 MIN

Entry Time: {entry_time.strftime('%H:%M:%S')} IST
Exit Time: {exit_time.strftime('%H:%M:%S')} IST

Price: {round(price,5)}
Support: {round(support,5)}
Resistance: {round(resistance,5)}

Strategy:
RSI + EMA + Candle + S/R Confirm
"""

    return msg

# ================= TELEGRAM =================
async def start(update, context):
    await update.message.reply_text("🔥 PRO BOT RUNNING...")

async def manual_signal(update, context):
    msg = format_signal()
    await update.message.reply_text(msg)

# ================= AUTO LOOP =================
async def auto_loop(app):
    while True:
        try:
            # ALERT
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Signal aa raha hai 3 min me...")

            await asyncio.sleep(180)

            # REAL SIGNAL
            msg = format_signal()
            await bot.send_message(chat_id=CHAT_ID, text=msg)

            await asyncio.sleep(60)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(10)

# ================= MAIN =================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", manual_signal))

    print("🔥 PRO BOT RUNNING...")

    asyncio.create_task(auto_loop(app))

    await app.run_polling()

# ================= RUN =================
if __name__ == "__main__":
    print("🔥 PRO BOT RUNNING...")
    app.run_polling()
