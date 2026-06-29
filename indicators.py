from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

def calculate_indicators(df):

    df["EMA20"] = EMAIndicator(
        close=df["close"],
        window=20
    ).ema_indicator()

    df["EMA50"] = EMAIndicator(
        close=df["close"],
        window=50
    ).ema_indicator()

    df["RSI"] = RSIIndicator(
        close=df["close"],
        window=14
    ).rsi()

    macd = MACD(df["close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    adx = ADXIndicator(
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )

    df["ADX"] = adx.adx()

    atr = AverageTrueRange(
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )

    df["ATR"] = atr.average_true_range()

    return df