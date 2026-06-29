def generate_signal(df, pattern):

    last = df.iloc[-1]

    score = 0
    reasons = []

    # EMA
    if last["EMA20"] > last["EMA50"]:
        score += 25
        reasons.append("EMA Bullish")
    else:
        score -= 25

    # MACD
    if last["MACD"] > last["MACD_SIGNAL"]:
        score += 25
        reasons.append("MACD Bullish")
    else:
        score -= 25

    # RSI
    if 50 < last["RSI"] < 70:
        score += 15
        reasons.append("Healthy RSI")
    elif last["RSI"] > 75:
        score -= 20
        reasons.append("Overbought")
    elif last["RSI"] < 30:
        score += 20
        reasons.append("Oversold")

    # ADX
    if last["ADX"] > 25:
        score += 20
        reasons.append("Strong Trend")
    else:
        score -= 10

    # Candlestick Pattern
    bullish = [
        "Hammer",
        "Bullish Engulfing"
    ]

    bearish = [
        "Shooting Star",
        "Bearish Engulfing"
    ]

    if pattern in bullish:
        score += 25
        reasons.append(pattern)

    elif pattern in bearish:
        score -= 25
        reasons.append(pattern)

    confidence = min(abs(score), 100)

    if score >= 60:
        signal = "🟢 BUY"
    elif score <= -60:
        signal = "🔴 SELL"
    else:
        signal = "⚪ NO TRADE"

    return signal, confidence, reasons