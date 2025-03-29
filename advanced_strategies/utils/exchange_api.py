import abc
import requests
import json
from typing import Dict, List

class ExchangeAPI(metaclass=abc.ABCMeta):
    """
    Abstract base class for exchange APIs.
    """
    def __init__(self, api_key: str, api_secret: str, base_url: str):
        """
        Initialize the exchange API.

        :param api_key: API key for the exchange
        :param api_secret: API secret for the exchange
        :param base_url: Base URL for the exchange API
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    @abc.abstractmethod
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a symbol.

        :param symbol: Symbol to retrieve data for
        :param start_date: Start date for the data
        :param end_date: End date for the data
        :return: Pandas DataFrame with the historical data
        """
        pass

    @abc.abstractmethod
    def get_current_price(self, symbol: str) -> float:
        """
        Get the current price for a symbol.

        :param symbol: Symbol to retrieve the current price for
        :return: Current price for the symbol
        """
        pass

    @abc.abstractmethod
    def place_order(self, symbol: str, quantity: float, side: str) -> Dict:
        """
        Place an order on the exchange.

        :param symbol: Symbol to place the order for
        :param quantity: Quantity to buy or sell
        :param side: Side of the order (buy or sell)
        :return: Dictionary with the order details
        """
        pass

    @abc.abstractmethod
    def get_account_balance(self) -> Dict:
        """
        Get the account balance.

        :return: Dictionary with the account balance details
        """
        pass

    def _sign_request(self, method: str, endpoint: str, params: Dict) -> Dict:
        """
        Sign a request with the API key and secret.

        :param method: HTTP method for the request
        :param endpoint: Endpoint for the request
        :param params: Parameters for the request
        :return: Signed request headers
        """
        timestamp = int(datetime.datetime.now().timestamp() * 1000)
        signature = hmac.new(self.api_secret.encode(), f"{method}{endpoint}{timestamp}{json.dumps(params)}".encode(), hashlib.sha256).hexdigest()
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "X-MBX-SECRET-KEY": self.api_secret,
            "X-MBX-TIMESTAMP": str(timestamp),
            "X-MBX-SIGNATURE": signature
        }
        return headers

    def _make_request(self, method: str, endpoint: str, params: Dict) -> Dict:
        """
        Make a request to the exchange API.

        :param method: HTTP method for the request
        :param endpoint: Endpoint for the request
        :param params: Parameters for the request
        :return: Response from the exchange API
        """
        headers = self._sign_request(method, endpoint, params)
        response = requests.request(method, f"{self.base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
