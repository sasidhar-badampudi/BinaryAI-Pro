import yfinance as yf

pair = "EURUSD=X"

data = yf.download(pair, period="1d", interval="1m")

print(data.tail())