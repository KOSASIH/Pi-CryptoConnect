import pandas as pd
import yfinance as yf

def load_market_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for ticker in tickers:
        data[ticker] = yf.download(ticker, start=start_date, end=end_date)['Close']
    return data
