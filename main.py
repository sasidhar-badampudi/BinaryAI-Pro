import os
import requests
import pandas as pd
from dotenv import load_dotenv

from indicators import calculate_indicators
from patterns import detect_pattern
from signal import generate_signal
from strategy import generate_signals
from backtest import run_backtest

# ===========================
# Load API Key
# ===========================

load_dotenv()
API_KEY = os.getenv("API_KEY")
print("API KEY:", API_KEY)
print("Length :", len(API_KEY) if API_KEY else 0)

# ===========================
# Settings
# ===========================

SYMBOL = "EUR/USD"
INTERVAL = "1min"

# ===========================
# Download Data
# ===========================

url = (
    f"https://api.twelvedata.com/time_series"
    f"?symbol={SYMBOL}"
    f"&interval={INTERVAL}"
    f"&outputsize=200"
    f"&apikey={API_KEY}"
)

response = requests.get(url)
data = response.json()

if "values" not in data:
    print("API Error")
    print(data)
    quit()

# ===========================
# Create DataFrame
# ===========================

df = pd.DataFrame(data["values"])

df = df.iloc[::-1].reset_index(drop=True)

for col in ["open", "high", "low", "close"]:
    df[col] = df[col].astype(float)

# ===========================
# Indicators
# ===========================

df = calculate_indicators(df)

# ===========================
# Historical Strategy
# ===========================

df = generate_signals(df)

# ===========================
# Current Candle Analysis
# ===========================

pattern = detect_pattern(df)

signal, confidence, reasons = generate_signal(df, pattern)

last = df.iloc[-1]

print("\n" + "=" * 50)
print("🚀 BinaryAI Pro v0.5")
print("=" * 50)

print(f"Pair        : {SYMBOL}")
print(f"Time        : {last['datetime']}")
print(f"Price       : {last['close']:.5f}")

print("\nIndicators")
print("-" * 50)
print(f"EMA20       : {last['EMA20']:.5f}")
print(f"EMA50       : {last['EMA50']:.5f}")
print(f"RSI         : {last['RSI']:.2f}")
print(f"MACD        : {last['MACD']:.5f}")
print(f"ADX         : {last['ADX']:.2f}")
print(f"ATR         : {last['ATR']:.5f}")

print("\nPattern")
print("-" * 50)
print(pattern)

print("\nReasons")
print("-" * 50)

if reasons:
    for reason in reasons:
        print("✔", reason)
else:
    print("No confirmations")

print("=" * 50)
print("Signal      :", signal)
print("Confidence  :", confidence, "%")
print("=" * 50)

# ===========================
# Backtest
# ===========================

df = run_backtest(df)