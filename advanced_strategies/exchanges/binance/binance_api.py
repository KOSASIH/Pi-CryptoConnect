import requests
import json
import hmac
import hashlib
import datetime
import pandas as pd

class BinanceAPI(ExchangeAPI):
    """
    Binance API implementation.
    """
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Binance API.

        :param api_key: API key for Binance
        :param api_secret: API secret for Binance
        """
        super().__init__(api_key, api_secret, "https://api.binance.com/api/v3/")

    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a symbol on Binance.

        :param symbol: Symbol to retrieve data for
        :param start_date: Start date for the data
        :param end_date: End date for the data
        :return: Pandas DataFrame with the historical data
        """
        params = {
            "symbol": symbol,
            "interval": "1m",
            "startTime": start_date,
            "endTime": end_date
        }
        response = self._make_request("GET", "klines", params)
        data = response["result"]
        df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
        return df

    def get_current_price(self, symbol: str) -> float:
        """
        Get the current price for a symbol on Binance.

        :param symbol: Symbol to retrieve the current price for
        :return: Current price for the symbol
        """
        params = {
            "symbol": symbol
        }
        response = self._make_request("GET", "ticker/price", params)
        return float(response["price"])

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict:
        """
        Place an order on Binance.

        :param symbol: Symbol to place the order for
        :param quantity: Quantity to buy or sell
        :param side: Side of the order (buy or sell)
        :return: Dictionary with the order details
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": self.get_current_price(symbol)
        }
        response = self._make_request("POST", "order", params)
        return response

    def get_account_balance(self) -> Dict:
        """
        Get the account balance on Binance.

        :return: Dictionary with the account balance details
        """
        response = self._make_request("GET", "account", {})
        return response["balances"]
