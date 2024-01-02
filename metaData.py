import yfinance as yf
import pandas as pd
import csv

def fetch_data(ticker_symbol):
    data_frames = []
    date_range = None
    try:
        stock = yf.Ticker(ticker_symbol)
        stock_data = stock.history(period='max')

        if not stock_data.empty:
            # Extract the 'Close' column and reset the index to keep date and closing price
            stock_data = stock_data[['Close']].reset_index()
            stock_data = stock_data.rename(columns={'Date': 'Date', 'Close': ticker_symbol})
            #stock_data.head()
            # data_frames.append(stock_data)

            # # Create a date range for the first stock
            # if date_range is None:
            #     date_range = stock_data['Date']
            # else:
            #     # Align date ranges, adding missing dates
            #     date_range = date_range.union(stock_data['Date'])

    except Exception as e:
        print(f"An error occurred for {ticker_symbol}: {e}")

    return stock_data

def store_data():

    filename = "C:/Users/Ketul/Desktop/Algo Trading - Copy/Symbols50.csv"
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for x in csvreader:
            try:
                # Set the ticker
                ticker = x[0]
                print(fetch_data(ticker).head())

            except:
                print(x, " Not available")

def get_stocks():
    filename = "C:/Users/Ketul/Desktop/Algo Trading - Copy/Symbols50.csv"
    potentials = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for x in csvreader:
            try:
                # Set the ticker
                ticker = x[0]
                data = fetch_data(ticker)
                cutOff = pd.Timestamp('2010-01-01 12:00:00').tz_localize('Asia/Kolkata')

                # Compare Timestamps
                if cutOff > data.loc[0][0]:
                    print(ticker)

            except Exception as e:
                print(e)

get_stocks()