import requests
import json
import hmac
import hashlib
import datetime
import pandas as pd

class CoinbaseProAPI(ExchangeAPI):
    """
    Coinbase Pro API implementation.
    """
    def __init__(self, api_key: str, api_secret: str, api_passphrase: str):
        """
        Initialize the Coinbase Pro API.

        :param api_key: API key for Coinbase Pro
        :param api_secret: API secret for Coinbase Pro
        :param api_passphrase: API passphrase for Coinbase Pro
        """
        super().__init__(api_key, api_secret, "https://api.pro.coinbase.com/")
        self.api_passphrase = api_passphrase

    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a symbol on Coinbase Pro.

        :param symbol: Symbol to retrieve data for
        :param start_date: Start date for the data
        :param end_date: End date for the data
        :return: Pandas DataFrame with the historical data
        """
        params = {
            "granularity": 60,  # 1 minute candles
            "start": start_date,
            "end": end_date
        }
        response = self._make_request("GET", f"products/{symbol}/candles", params)
        data = response
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        return df

    def get_current_price(self, symbol: str) -> float:
        """
        Get the current price for a symbol on Coinbase Pro.

        :param symbol: Symbol to retrieve the current price for
        :return: Current price for the symbol
        """
        response = self._make_request("GET", f"products/{symbol}/ticker")
        return float(response["price"])

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict:
        """
        Place an order on Coinbase Pro.

        :param symbol: Symbol to place the order for
        :param quantity: Quantity to buy or sell
        :param side: Side of the order (buy or sell)
        :return: Dictionary with the order details
        """
        params = {
            "type": "limit",
            "side": side,
            "product_id": symbol,
            "size": quantity,
            "price": self.get_current_price(symbol)
        }
        response = self._make_request("POST", "orders", params)
        return response

    def get_account_balance(self) -> Dict:
        """
        Get the account balance on Coinbase Pro.

        :return: Dictionary with the account balance details
        """
        response = self._make_request("GET", "accounts")
        return response

    def _make_request(self, method: str, endpoint: str, params: Dict = {}) -> Dict:
        """
        Make a request to the Coinbase Pro API.

        :param method: HTTP method to use (GET, POST, etc.)
        :param endpoint: API endpoint to call
        :param params: Parameters to pass with the request
        :return: Response from the API
        """
        timestamp = str(int(datetime.datetime.now().timestamp()))
        message = timestamp + method + endpoint + json.dumps(params)
        signature = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json"
        }
        response = requests.request(method, self.base_url + endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
