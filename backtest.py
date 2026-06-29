def run_backtest(df):
    """
    Backtest signals using a 1-candle expiry.
    """

    trades = 0
    wins = 0
    losses = 0

    results = []

    for i in range(len(df) - 1):

        signal = df.iloc[i]["SIGNAL"]

        if signal == "NO TRADE":
            results.append("")
            continue

        entry = df.iloc[i]["close"]
        exit_price = df.iloc[i + 1]["close"]

        trades += 1

        if signal == "BUY":

            if exit_price > entry:
                wins += 1
                results.append("WIN")
            else:
                losses += 1
                results.append("LOSS")

        elif signal == "SELL":

            if exit_price < entry:
                wins += 1
                results.append("WIN")
            else:
                losses += 1
                results.append("LOSS")

    # Last candle has no future candle
    results.append("")

    df["RESULT"] = results

    if trades == 0:
        win_rate = 0
    else:
        win_rate = (wins / trades) * 100

    print("\n" + "=" * 50)
    print("📊 BinaryAI Pro v0.5 Backtest")
    print("=" * 50)
    print(f"Total Trades : {trades}")
    print(f"Wins         : {wins}")
    print(f"Losses       : {losses}")
    print(f"Win Rate     : {win_rate:.2f}%")
    print("=" * 50)

    print("\nLast 10 Trades")
    print(df[["datetime", "close", "SIGNAL", "RESULT"]].tail(10))

    return df