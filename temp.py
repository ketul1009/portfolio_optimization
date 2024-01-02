import yfinance as yf

data = yf.download('SBIN.NS', '2022-03-31', '2023-03-31')
print(data['High'].max())