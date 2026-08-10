# main.py (improved)
import os
import logging
from typing import Dict, Any

import requests
import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from telegram import Bot

# Prefer loading secrets from env (or from a local, gitignored config.py).
TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # store as string; convert to int before use

# Parameters / constants
SYMBOL = "XAU/USD"
INTERVAL = "15min"
OUTPUTSIZE = 100
EMA_SHORT = 20
EMA_LONG = 50
RSI_PERIODDirect answer: This script downloads recent XAU/USD (gold) 15-minute price data from Twelve Data, computes EMA(20), EMA(50), RSI(14) and MACD, derives a simple BUY/SELL/WAIT signal from those indicators, and attempts to send the result via Telegram. Below I explain what each part does, point out functional and security problems, and provide a corrected example and suggestions.

What the code does (high-level)
- Fetches 15-minute OHLC time series for XAU/USD from Twelve Data.
- Loads the returned "values" into a pandas DataFrame and reverses the order so rows go oldest→newest.
- Converts the close prices to float and computes EMA20 = 14
REQUEST_TIMEOUT = 10  # seconds

logging.basic, EMA50, RSI(14) and MACD.
-Config(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_time_series(api_key: str, symbol Sets signal = "BUY" if EMA20 > EMA50, RSI > 50 and MACD > MACD signal; sets "SELL" when the opposite; otherwise: str, interval: str, outputsize: int) -> Dict[str, Any]:
    if not api_key:
        raise ValueError("TWELVEDATA_API_KEY not set")
    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={symbol}&interval={interval}&apikey={api_key}&outputsize={outputsize}"
    )
    resp = requests "WAIT".
- Builds a message with the latest price and indicator values and attempts to send it via Telegram.
- Prints "Selesai" at the end.

Line-by-line explanation and notes (referring to the file you provided)
- Lines 1–6: imports. requests, pandas, ta indicators, and Telegram Bot are imported; config.BOT_TOKEN and CHAT.get(url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    if "values" not in data:
        raise RuntimeError(f"Unexpected response from API: {data}")
    return data


def build_dataframe(values: list) -> pd.DataFrame:
    df = pd.DataFrame(values)
    # API returns newest-first; reverse to chronological order and reset index
    df = df.iloc_ID are imported but never[::-1].reset_index(drop=True)
    # Convert numeric columns
    df["close"] = df["close"].astype(float)
    # Parse time column if present
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime actually used (the script instead hard-codes tokens later).
- Line 8: API_KEY")
    return df


def compute_indicators(df: pd.Data = 8909766487:AAE9jjWqwj9X4Qm2ziz_BuNcVsMjtoQD9T8
  - Problem: this is not a quoted string, so the code as shown is a syntax error. API keys and tokens must be strings (quoted).
  - Security: the API key (and other tokens below) appear in the file — that's aFrame):
    close = df["close"]
    ema_short = EMAIndicator(close, EMA_SHORT).ema_indicator()
    ema secret leak risk. Secrets should not be committed to source.
- Line 10: builds the Twelve Data time_series URL with that_long = EMAIndicator(close, EMA_LONG).ema_indicator API key and outputsize=100.
- Line 12: data = requests.get(url).json()
  - Problem: no error handling. If requests fails or the API returns an error JSON, this will later raise KeyError.
- Line 14: df = pd.DataFrame(data["()
    rsi = RSIIndicator(close, RSI_PERIOD).rsi()
    macd = MACD(close)  # can pass fastvalues"])
  - Assumes the response contains "values". If the request failed or the API returned an error message, KeyError will/slow/signal occur.
- Line 16: df = df.iloc[::-1]
  - Reverses rows so index order is oldest → newest (Twelve Data often returns newest→oldest).
- Line 18: df["close"] = df["close"].astype(float)
  params if needed
    return ema_short, ema_long, r - Converts the close column to floats.
- Lines 20–26: compute indicators
  - EMAIndicator(df["close"], 20).ema_indicator() → series for EMA20
  - EMAIndicator(df["closesi, macd


def decide_signal(ema_short, ema_long, rsi, macd) -> str:
    last = -1
    if (
        ema"], 50).ema_indicator() → EMA50
  -_short.iloc[last] > ema_long.iloc[last]
        and rsi.iloc[last] > 50
        and macd.macd().iloc[last] > macd.macd_signal().iloc[last]
    ):
        return "BUY"
    if (
        ema_short.iloc[last] < ema_long.iloc[last]
        RSIIndicator(df["close"], 14).rsi() → RSI series
  - macd = MACD(df["close"]) → MACD object; macd.macd() and macd.macd_signal()
- Lines 28–34: signal logic
  - Default "WAIT".
  - BUY if EMA20 > EMA50 and RSI > 50 and MACD > MAC and rsi.iloc[last] < 50
        and macd.macd().iloc[last] < macd.macd_signal().iloc[last]
    ):
        return "SELL"
    return "WAIT"


def format_message(symbol: str, price: float, signal: str, ema_short, ema_long, rsi) -> str:
    return (
        f"📊 {symbol}\n\n"
        f"Signal : {signal}\n\n"
        f"Harga : {price}\n\n"
       D signal (last row values).
  - SELL if EMA20 < EMA50 and RSI < 50 and MACD < MACD signal (last row values).
  - This is a simple crossover + momentum rule.
- Line 36: price = df["close"].iloc[-1] — latest close.
- Lines 38–50 f"EMA{EMA_SHORT} : {round(ema_short.iloc[-1], 2)}\n\n"
        f"EMA{EMA_LONG} : {round(ema_long.iloc[-1], : build multi-line pesan string with symbol, signal, price, EMA20, EMA50, RSI.
- Line 2)}\n\n"
        f"RSI : {round(rsi.iloc[-1], 2)}\n"
    )


def52: bot=Bot(a69d0c1780cb462 send_telegram_message(bot_token: str, chat_id: str, text: str):
    if not bot_token or not chat_id:
        raise ValueError("Telegram credentials not provided")
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=int(chat_id), text=text)


def main():
    try:
        raw = fetch_time_series(TWELVEDATA_API_KEY, SYMBOL, INTERVAL, OUTPUTSIZE)
        df = build_dataframe(raw["valuesd9f4817"])
        ema_short, ema_long, rsi, macd = compute_indicators(df)
        signal = decide_signal(emab8afa20e0e)
_short, ema_long, rsi, macd)
        price = df["close"].iloc[-1]
        message = format_message(SYMBOL, price, signal, ema_short, ema_long, rsi)
         - Problem: logger.info("Signal: %s, Price: %s", signal, price)
        # Use configured values (env/config)
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    except Exception as exc:
        logger.exception("Failed to fetch or send signal: %s", exc)


if __name__ == "__main__":
    main()
