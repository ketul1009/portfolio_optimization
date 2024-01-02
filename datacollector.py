import pandas as pd
from tradingview_ta import TA_Handler, Interval
import yfinance as yf

# Load the Excel file with openpyxl engine
tickers = ["WIPRO", "TITAN", "CIPLA", "BPCL", "MARUTI", "GRASIM", "ITC", "HEROMOTOCO", "ULTRACEMCO",
 "INDUSINDBK", "DRREDDY", "JSWSTEEL", "KOTAKBANK", "HCLTECH", "COALINDIA", "ADANIPORTS", 
 "ADANIENT", "TECHM", "RELIANCE", "SBIN", "INFY", "BAJFINANCE", "HINDUNILVR",
 "SUNPHARMA", "AXISBANK", "BAJAJ-AUTO", "DIVISLAB", "EICHERMOT", "HINDUNILVR", "ONGC", "POWERGRID",
 "TATACONSUM", "TATAMOTORS", "TCS", "UPL"]

targetPrices = []

for ticker in tickers:
    try:
        #Perform Fundamental Analysis
        file = 'Data/'+ticker+'.xlsx'
        data = pd.read_excel(file, sheet_name='Data Sheet')
        begining = data.loc[28][7]
        ending = data.loc[28][9]
        cagr = (ending/begining)**(1/3)-1
        projectIncome = (cagr+1)*ending
        numberShares = data.loc[68][9]
        price = data.loc[88][9]
        actualPrice = data.loc[88][10]
        projectedEps = projectIncome/numberShares
        eps = ending/numberShares
        pe = price/eps
        targetPrice = projectedEps*pe
        xReturns = ((targetPrice/price)-1)*100

        #To get Last Traded Price
        output = TA_Handler(
            symbol=ticker,
            screener="India",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY
        )
        data = yf.download(ticker+".NS", '2022-03-31', '2023-03-31')
        drawdown = ((data['High'].min()/price)-1)*100
        runUp = ((data['High'].max()/price)-1)*100

        ltp = output.get_analysis().indicators['close']
        temp = { 'Stock': ticker, 'CMP(22)' : price, 'Target': round(targetPrice,0), 'xReturn' : round(xReturns, 2), 
                 'LTP': round(ltp, 2), 'High': round(data['High'].max(), 2),
                 'CMP(23)' : actualPrice,
                 'Target Hit' : data['High'].max() >= targetPrice,
                 'Drawdown' : drawdown,
                 'Run-up' : runUp,
                 'Range': round(runUp-drawdown, 2)
               }
        targetPrices.append(temp)
        print(ticker+" completed")
    except:
        print("Error occured: "+ticker)

df = pd.DataFrame(targetPrices)
df = df.loc[df['xReturn'] > 19]
portfolio_data = []

weights = [0.04607126, 0.10531979, 0.40861803, 0.00804356, 0.08876231, 0.00153695, 0.02704314, 0.18751117, 0.1270938]

for i in range(len(weights)):
    stock_data = df.iloc[i]  # Select the i-th row from the filtered DataFrame
    quantity = round((100000 * weights[i]) / stock_data['CMP(22)'], 0)  # Replace 'Column_Name' with the actual column name
    buy_value = quantity * stock_data['CMP(22)']
    return_value = quantity * (stock_data['CMP(23)'] - stock_data['CMP(22)'])

    portfolio_data.append({
        'Stock': stock_data['Stock'],  # Replace 'Stock' with the actual column name
        'Quantity': round(quantity, 0),
        'Buy-Value': round(buy_value, 2),
        'Return': round(return_value, 2)
    })

# Create the portfolio DataFrame from the list of dictionaries
portfolio = pd.DataFrame(portfolio_data)

print(portfolio)
