import requests
import json
import hmac
import hashlib
import datetime
import pandas as pd

class HuobiAPI(ExchangeAPI):
    """
    Huobi API implementation.
    """
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the Huobi API.

        :param api_key: API key for Huobi
        :param api_secret: API secret for Huobi
        """
        super().__init__(api_key, api_secret, "https://api.huobi.pro/api/v1/")

    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a symbol on Huobi.

        :param symbol: Symbol to retrieve data for
        :param start_date: Start date for the data
        :param end_date: End date for the data
        :return: Pandas DataFrame with the historical data
        """
        params = {
            "symbol": symbol,
            "period": "1min",
            "size": 1000,
            "from": int(pd.to_datetime(start_date).timestamp() * 1000),
            "to": int(pd.to_datetime(end_date).timestamp() * 1000)
        }
        response = self._make_request("GET", "market/history/kline", params)
        data = response["data"]
        df = pd.DataFrame(data, columns=["id", "open", "close", "low", "high", "amount", "vol", "count"])
        df["id"] = pd.to_datetime(df["id"], unit="ms")
        return df

    def get_current_price(self, symbol: str) -> float:
        """
        Get the current price for a symbol on Huobi.

        :param symbol: Symbol to retrieve the current price for
        :return: Current price for the symbol
        """
        response = self._make_request("GET", f"market/detail/merged", {"symbol": symbol})
        return float(response["tick"]["close"])

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict:
        """
        Place an order on Huobi.

        :param symbol: Symbol to place the order for
        :param quantity: Quantity to buy or sell
        :param side: Side of the order (buy or sell)
        :return: Dictionary with the order details
        """
        params = {
            "account-id": self.api_key,
            "amount": quantity,
            "price": self.get_current_price(symbol),
            "source": "api",
            "symbol": symbol,
            "type": side
        }
        response = self._make_request("POST", "order/orders/place", params)
        return response

    def get_account_balance(self) -> Dict:
        """
        Get the account balance on Huobi.

        :return: Dictionary with the account balance details
        """
        response = self._make_request("GET", "account/accounts/{account-id}/balance".format(account-id=self.api_key))
        return response

    def _make_request(self, method: str, endpoint: str, params: Dict = {}) -> Dict:
        """
        Make a request to the Huobi API.

        :param method: HTTP method to use (GET, POST, etc.)
        :param endpoint: API endpoint to call
        :param params: Parameters to pass with the request
        :return: Response from the API
        """
        timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
        message = timestamp + method + endpoint + json.dumps(params)
        signature = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {
            "Api-Key": self.api_key,
            "Api-Sign": signature,
            "Api-Timestamp": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.request(method, self.base_url + endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
