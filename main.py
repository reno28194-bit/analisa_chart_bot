import requests
import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from telegram import Bot
from config import BOT_TOKEN, CHAT_ID

API_KEY = 8909766487:AAE9jjWqwj9X4Qm2ziz_BuNcVsMjtoQD9T8

url = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=15min&apikey={API_KEY}&outputsize=100"

data = requests.get(url).json()

df = pd.DataFrame(data["values"])

df = df.iloc[::-1]

df["close"] = df["close"].astype(float)

ema20 = EMAIndicator(df["close"],20).ema_indicator()

ema50 = EMAIndicator(df["close"],50).ema_indicator()

rsi = RSIIndicator(df["close"],14).rsi()

macd = MACD(df["close"])

signal = "WAIT"

if ema20.iloc[-1] > ema50.iloc[-1] and rsi.iloc[-1] > 50 and macd.macd().iloc[-1] > macd.macd_signal().iloc[-1]:
    signal="BUY"

elif ema20.iloc[-1] < ema50.iloc[-1] and rsi.iloc[-1] <50 and macd.macd().iloc[-1] < macd.macd_signal().iloc[-1]:
    signal="SELL"

price=df["close"].iloc[-1]

pesan=f"""
📊 XAU/USD

Signal : {signal}

Harga : {price}

EMA20 : {round(ema20.iloc[-1],2)}

EMA50 : {round(ema50.iloc[-1],2)}

RSI : {round(rsi.iloc[-1],2)}
"""

bot=Bot(BOT_TOKEN)

bot.send_message(chat_id=CHAT_ID,text=pesan)

print("Selesai")
