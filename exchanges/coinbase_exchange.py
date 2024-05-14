# pi_cryptoconnect/exchanges/coinbase_exchange.py

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO)


class CoinbaseExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.base_url = "https://api.coinbase.com/v2"

    def _get_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}", "CB-VERSION": "2021-08-07"}

    def _handle_response(self, response: requests.Response) -> List[Dict]:
        response.raise_for_status()
        return response.json()["data"]["candles"]

    def get_historical_klines(
        self, symbol: str, interval: str, start_time: str, end_time: str
    ) -> List[Dict]:
        """
        Retrieves historical klines data from Coinbase.

        Args:
            symbol (str): The symbol to fetch the klines data for.
            interval (str): The interval of the klines data.
            start_time (str): The start time of the data range in ISO 8601 format.
            end_time (str): The end time of the data range in ISO 8601 format.

        Returns:
            List[Dict]: A list of dictionaries containing the klines data.
        """
        url = f"{self.base_url}/products/{symbol}/candles"
        params = {"granularity": interval, "start": start_time, "end": end_time}
        headers = self._get_headers()

        try:
            response = self.session.get(url, params=params, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def get_account_info(self) -> Dict:
        """
        Retrieves account information from Coinbase.

        Returns:
            Dict: A dictionary containing the account information.
        """
        url = f"{self.base_url}/accounts"
        headers = self._get_headers()

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["data"][0]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def place_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> Dict:
        """
        Places an order on Coinbase.

        Args:
            symbol (str): The symbol to place the order for.
            side (str): The side of the order (buy or sell).
            quantity (float): The quantity of the order.
            price (float): The price of the order.

        Returns:
            Dict: A dictionary containing the order information.
        """
        url = f"{self.base_url}/orders"
        headers = self._get_headers()
        data = {
            "product_id": symbol,
            "side": side,
            "size": str(quantity),
            "price": str(price),
            "type": "limit",
        }

        try:
            response = self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing order: {e}")
            raise
