def detect_pattern(df):

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Candle body
    last_body = abs(last["close"] - last["open"])
    prev_body = abs(prev["close"] - prev["open"])

    # Bullish Engulfing
    if (
        prev["close"] < prev["open"] and
        last["close"] > last["open"] and
        last["open"] < prev["close"] and
        last["close"] > prev["open"]
    ):
        return "Bullish Engulfing"

    # Bearish Engulfing
    if (
        prev["close"] > prev["open"] and
        last["close"] < last["open"] and
        last["open"] > prev["close"] and
        last["close"] < prev["open"]
    ):
        return "Bearish Engulfing"

    # Doji
    if last_body <= (last["high"] - last["low"]) * 0.1:
        return "Doji"

    # Hammer
    lower_shadow = min(last["open"], last["close"]) - last["low"]
    upper_shadow = last["high"] - max(last["open"], last["close"])

    if lower_shadow > last_body * 2 and upper_shadow < last_body:
        return "Hammer"

    # Shooting Star
    if upper_shadow > last_body * 2 and lower_shadow < last_body:
        return "Shooting Star"

    return "None"