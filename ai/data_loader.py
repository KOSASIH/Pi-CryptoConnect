import pandas as pd
import yfinance as yf
import ccxt
import asyncio
import logging
from pi_cryptoconnect.integrations.ccxt import get_exchange_markets

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    def __init__(self, exchange, tickers, start_date, end_date, timeframe='1d'):
        self.exchange = exchange
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.cache = {}

    async def load_market_data(self):
        tasks = []
        for ticker in self.tickers:
            tasks.append(self.fetch_data(ticker))
        data = await asyncio.gather(*tasks)
        return pd.DataFrame(data).T

    async def fetch_data(self, ticker):
        if ticker in self.cache:
            logging.info(f"Fetching {ticker} from cache.")
            return self.cache[ticker]

        try:
            if self.exchange == 'yahoo':
                logging.info(f"Fetching {ticker} data from Yahoo Finance.")
                data = yf.download(ticker, start=self.start_date, end=self.end_date)['Close']
                self.cache[ticker] = data
                return data
            elif self.exchange == 'ccxt':
                logging.info(f"Fetching {ticker} data from CCXT.")
                exchange_markets = get_exchange_markets()
                market = exchange_markets.get(ticker)
                if market is None:
                    logging.error(f"Market for {ticker} not found.")
                    return pd.Series(dtype='float64')

                ohlcv = await self.fetch_ohlcv(market)
                self.cache[ticker] = ohlcv['close']
                return ohlcv['close']
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
            return pd.Series(dtype='float64')

    async def fetch_ohlcv(self, market):
        exchange = ccxt.binance()
        since = exchange.parse8601(self.start_date)
        ohlcv = await exchange.fetch_ohlcv(market, timeframe=self.timeframe, since=since, limit=1000)
        ohlcv_df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        ohlcv_df['timestamp'] = pd.to_datetime(ohlcv_df['timestamp'], unit='ms')
        return ohlcv_df

def load_market_data(tickers, start_date, end_date, exchange='yahoo', timeframe='1d'):
    data_loader = DataLoader(exchange, tickers, start_date, end_date, timeframe)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(data_loader.load_market_data())
    return data

# Example usage
if __name__ == "__main__":
    tickers = ['AAPL', 'BTC/USDT']  # Example tickers
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    exchange = 'ccxt'  # or 'yahoo'
    timeframe = '1d'  # For CCXT data

    market_data = load_market_data(tickers, start_date, end_date, exchange, timeframe)
    print(market_data)
