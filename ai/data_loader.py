import pandas as pd
import yfinance as yf
import ccxt
import asyncio
from pi_cryptoconnect.integrations.ccxt import get_exchange_markets

class DataLoader:
    def __init__(self, exchange, tickers, start_date, end_date):
        self.exchange = exchange
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

    async def load_market_data(self):
        data = pd.DataFrame()
        for ticker in self.tickers:
            if self.exchange == 'yahoo':
                data[ticker] = yf.download(ticker, start=self.start_date, end=self.end_date)['Close']
            elif self.exchange == 'ccxt':
                exchange_markets = get_exchange_markets()
                market = exchange_markets[ticker]
                ohlcv = await self.fetch_ohlcv(market, self.start_date, self.end_date)
                data[ticker] = ohlcv['close']
        return data

    async def fetch_ohlcv(self, market, start_date, end_date):
        exchange = ccxt.binance()
        ohlcv = await exchange.fetch_ohlcv(market, timeframe='1d', since=start_date, limit=1000)
        ohlcv_df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        ohlcv_df['timestamp'] = pd.to_datetime(ohlcv_df['timestamp'], unit='ms')
        return ohlcv_df

def load_market_data(tickers, start_date, end_date, exchange='yahoo'):
    data_loader = DataLoader(exchange, tickers, start_date, end_date)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(data_loader.load_market_data())
    return data
