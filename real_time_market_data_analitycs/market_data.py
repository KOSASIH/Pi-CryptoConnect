# market_data.py

import requests
import json
import pandas as pd

class MarketData:
    """
    Real-time market data analysis.
    """
    def __init__(self, api_keys: Dict):
        """
        Initialize the market data analysis.

        :param api_keys: Dictionary of API keys for different data sources
        """
        self.api_keys = api_keys
        self.data_sources = {
            "CoinMarketCap": CoinMarketCap(self.api_keys["CoinMarketCap"]),
            "CryptoCompare": CryptoCompare(self.api_keys["CryptoCompare"]),
            "AlphaVantage": AlphaVantage(self.api_keys["AlphaVantage"])
        }

    def get_realtime_data(self, symbol: str) -> pd.DataFrame:
        """
        Get real-time market data for a symbol.

        :param symbol: Symbol to retrieve data for
        :return: Pandas DataFrame with the real-time market data
        """
        data = {}
        for source, api in self.data_sources.items():
            data[source] = api.get_realtime_data(symbol)
        df = pd.DataFrame(data)
        return df

class CoinMarketCap:
    """
    CoinMarketCap API implementation.
    """
    def __init__(self, api_key: str):
        """
        Initialize the CoinMarketCap API.

        :param api_key: API key for CoinMarketCap
        """
        self.api_key = api_key
        self.base_url = "https://pro-api.coinmarketcap.com/v1/"

    def get_realtime_data(self, symbol: str) -> Dict:
        """
        Get real-time market data for a symbol on CoinMarketCap.

        :param symbol: Symbol to retrieve data for
        :return: Dictionary with the real-time market data
        """
        params = {
            "symbol": symbol,
            "convert": "USD"
        }
        response = requests.get(self.base_url + "cryptocurrency/quotes/latest", params=params, headers={"X-CMC_PRO_API_KEY": self.api_key})
        return response.json()["data"]

class CryptoCompare:
    """
    CryptoCompare API implementation.
    """
    def __init__(self, api_key: str):
        """
        Initialize the CryptoCompare API.

        :param api_key: API key for CryptoCompare
        """
        self.api_key = api_key
        self.base_url = "https://min-api.cryptocompare.com/data/"

    def get_realtime_data(self, symbol: str) -> Dict:
        """
        Get real-time market data for a symbol on CryptoCompare.

        :param symbol: Symbol to retrieve data for
        :return: Dictionary with the real-time market data
        """
        params = {
            "fsym": symbol,
            "tsyms": "USD"
        }
        response = requests.get(self.base_url + "price", params=params, headers={"Apikey": self.api_key})
        return response.json()

class AlphaVantage:
    """
    Alpha Vantage API implementation.
    """
    def __init__(self, api_key: str):
        """
        Initialize the Alpha Vantage API.

        :param api_key: API key for Alpha Vantage
        """
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query?"

    def get_realtime_data(self, symbol: str) -> Dict:
        """
        Get real-time market data for a symbol on Alpha Vantage.

        :param symbol: Symbol to retrieve data for
        :return: Dictionary with the real-time market data
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()["Global Quote"]
