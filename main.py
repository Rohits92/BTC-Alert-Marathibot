
import telebot
import pandas as pd
import requests
from datetime import datetime
import time

# Telegram bot token
TOKEN = "8077447364:AAHHJOQe86FPrSd5mf_dUTn7iZJ2cHKLr8Y"
CHAT_ID = "6607759141"  # Rohit Dhote
bot = telebot.TeleBot(TOKEN)

def fetch_binance_data(symbol="BTCUSDT", interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url).json()
    df = pd.DataFrame(response, columns=[
        "timestamp", "open", "high", "low", "close", "volume", "_", "_", "_", "_", "_", "_"
    ])
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    return df

def detect_bos(df):
    if df['high'].iloc[-2] < df['high'].iloc[-1] and df['low'].iloc[-2] > df['low'].iloc[-1]:
        return "Break of Structure (BOS) - BUY"
    elif df['low'].iloc[-2] > df['low'].iloc[-1] and df['high'].iloc[-2] < df['high'].iloc[-1]:
        return "Change of Character (CHoCH) - SELL"
    else:
        return None

def send_trade_alert():
    df = fetch_binance_data()
    signal = detect_bos(df)
    price = df['close'].iloc[-1]

    if signal:
        msg = f"🧠 *SMC सिग्नल आढळले!*
\n📌 प्रकार: `{signal}`\n⏰ Timeframe: 1H\n📊 प्राईस: {price}\n📅 वेळ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n🚨 कृपया चार्ट तपासा!"
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

# Infinite loop to check hourly
while True:
    send_trade_alert()
    time.sleep(3600)
