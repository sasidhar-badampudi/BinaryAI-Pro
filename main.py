from strategy import generate_signals
from backtest import run_backtest
df = calculate_indicators(df)
df = generate_signals(df)
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
import requests
import pandas as pd

from indicators import calculate_indicators
from signal import generate_signal
from patterns import detect_pattern

# ===========================
# BinaryAI Pro v0.4
# ===========================

SYMBOL = "EUR/USD"
INTERVAL = "1min"

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

df = pd.DataFrame(data["values"])

# Oldest → Newest
df = df.iloc[::-1].reset_index(drop=True)

# Convert to float
for col in ["open", "high", "low", "close"]:
    df[col] = df[col].astype(float)

# ===========================
# Calculate Indicators
# ===========================

df = calculate_indicators(df)

# ===========================
# Detect Candle Pattern
# ===========================

pattern = detect_pattern(df)

# ===========================
# Generate Signal
# ===========================

signal, confidence, reasons = generate_signal(df, pattern)

last = df.iloc[-1]

print("\n" + "=" * 45)
print("🚀 BinaryAI Pro v0.4")
print("=" * 45)

print(f"Pair        : {SYMBOL}")
print(f"Time        : {last['datetime']}")
print(f"Price       : {last['close']:.5f}")

print("\nIndicators")
print("-" * 45)
print(f"EMA20       : {last['EMA20']:.5f}")
print(f"EMA50       : {last['EMA50']:.5f}")
print(f"RSI         : {last['RSI']:.2f}")
print(f"MACD        : {last['MACD']:.5f}")
print(f"ADX         : {last['ADX']:.2f}")
print(f"ATR         : {last['ATR']:.5f}")

print("\nPattern")
print("-" * 45)
print(pattern)
print("\nPattern Score")
print("-" * 45)

if pattern and pattern != "None" and pattern != "No Pattern":
    print(f"✅ {pattern}")
else:
    print("❌ No Pattern Found")
print("\nReasons")
print("-" * 45)

if reasons:
    for reason in reasons:
        print("✔", reason)

else:
    print("No confirmations")
print("=" * 40)
print("Signal     :", signal)
print("Confidence :", confidence, "%")

print("=" * 40)

print("\nDecision")
print("-" * 45)
print(signal)

print("\nConfidence")
print("-" * 45)
print(f"{confidence}%")

print("=" * 45)
from backtest import run_backtest
run_backtest(df)