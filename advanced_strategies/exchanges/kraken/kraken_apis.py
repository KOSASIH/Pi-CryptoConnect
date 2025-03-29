import requests
import json
import hmac
import hashlib
import datetime
import pandas as pd

class KrakenAPI(ExchangeAPI):
    """
    Kraken API implementation.
    """
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Kraken API.

        :param api_key: API key for Kraken
        :param api_secret: API secret for Kraken
        """
        super().__init__(api_key, api_secret, "https://api.kraken.com/0/public/")

    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a symbol on Kraken.

        :param symbol: Symbol to retrieve data for
        :param start_date: Start date for the data
        :param end_date: End date for the data
        :return: Pandas DataFrame with the historical data
        """
        params = {
            "pair": symbol,
            "interval": 1,
            "since": int(pd.to_datetime(start_date).timestamp())
        }
        response = self._make_request("GET", "OHLC", params)
        data = response["result"][symbol]
        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    def get_current_price(self, symbol: str) -> float:
        """
        Get the current price for a symbol on Kraken.

        :param symbol: Symbol to retrieve the current price for
        :return: Current price for the symbol
        """
        params = {
            "pair": symbol
        }
        response = self._make_request("GET", "Ticker", params)
        return float(response["result"][symbol]["c"][0])

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict:
        """
        Place an order on Kraken.

        :param symbol: Symbol to place the order for
        :param quantity: Quantity to buy or sell
        :param side: Side of the order (buy or sell)
        :return: Dictionary with the order details
        """
        params = {
            "pair": symbol,
            "type": side,
            "ordertype": "limit",
            "price": self.get_current_price(symbol),
            "volume": quantity
        }
        response = self._make_request("POST", "Order", params)
        return response

    def get_account_balance(self) -> Dict:
        """
        Get the account balance on Kraken.

        :return: Dictionary with the account balance details
        """
        response = self._make_request("POST", "Balance", {})
        return response["result"]
