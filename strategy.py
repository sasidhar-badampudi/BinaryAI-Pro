def generate_signals(df):
    """
    Generate BUY / SELL / NO TRADE signal
    for every candle in the dataframe.
    """

    signals = []
    confidences = []

    for i in range(len(df)):

        if i < 50:
            signals.append("NO TRADE")
            confidences.append(0)
            continue

        row = df.iloc[i]

        score = 0

        # EMA
        if row["EMA20"] > row["EMA50"]:
            score += 25
        else:
            score -= 25

        # MACD
        if row["MACD"] > row["MACD_SIGNAL"]:
            score += 25
        else:
            score -= 25

        # RSI
        if 50 < row["RSI"] < 70:
            score += 15
        elif row["RSI"] > 75:
            score -= 20
        elif row["RSI"] < 30:
            score += 20

        # ADX
        if row["ADX"] > 25:
            score += 20
        else:
            score -= 10

        confidence = min(abs(score), 100)

        if score >= 60:
            signal = "BUY"
        elif score <= -60:
            signal = "SELL"
        else:
            signal = "NO TRADE"

        signals.append(signal)
        confidences.append(confidence)

    df["SIGNAL"] = signals
    df["CONFIDENCE"] = confidences

    return df