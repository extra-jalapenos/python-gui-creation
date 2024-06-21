import os
import pandas as pd
import datetime as dt
import yfinance as yf

#%%

def fetch_data(ticker, start_date, end_date):
    """Fetches stock data from Yahoo Finance and saves it to an Excel file."""
    try:
        data = yf.download(ticker, start_date, end_date)
        data.reset_index(inplace=True)
        data.to_excel("stock_data.xlsx", index=False)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Check if stock_data.xlsx exists
if not os.path.exists("stock_data.xlsx"):
    initial_data = fetch_data('AAPL', dt.datetime(2023, 1, 1), dt.datetime.now())
else:
    # If it exists, read it into the DataFrame
    initial_data = pd.read_excel("stock_data.xlsx")
    
#%%