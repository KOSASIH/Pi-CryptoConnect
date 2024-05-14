# pi_cryptoconnect/bittrex_exchange.py

import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class BittrexExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.base_url = "https://api.bittrex.com/v3"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json"
        }

    def _generate_signature(self, url: str, data: Dict) -> str:
        message = f"{url}\n{self._encode_data(data)}".encode()
        signature = hmac.new(self.api_secret.encode(), message, hashlib.sha512).hexdigest()
        return signature

    def _encode_data(self, data: Dict) -> str:
        return "&".join([f"{k}={v}" for k, v in sorted(data.items())])

    def _handle_response(self, response: requests.Response) -> List[Dict]:
        response.raise_for_status()
        return response.json()["result"]

    def get_historical_klines(self, symbol: str, interval: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Retrieves historical klines data from Bittrex.

        Args:
            symbol (str): The symbol to fetch the klines data for.
            interval (str): The interval of the klines data.
            start_time (int): The start time of the data range.
            end_time (int): The end time of the data range.

        Returns:
            List[Dict]: A list of dictionaries containing the klines data.
        """
        url = f"{self.base_url}/markets/{symbol}/candles"
        data = {
            "marketSymbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "take": 1000
        }
        headers = self._get_headers()
        signature = self._generate_signature(url, data)

        try:
            response = self.session.get(url, params=data, headers={**headers, "apisign": signature})
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def get_account_info(self) -> Dict:
        """
        Retrieves account information from Bittrex.

        Returns:
            Dict: A dictionary containing the account information.
        """
        url = f"{self.base_url}/account/balances"
        headers = self._get_headers()
        headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["result"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def place_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """
        Places an order on Bittrex.

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
        headers["Authorization"] = f"Bearer {self.api_key}"
        data = {
            "marketSymbol": symbol,"quantity": str(quantity),
            "limit": str(price),
            "orderType": "LIMIT" if side == "buy" else "LIMIT_SELL",
            "timeInForce": "GOOD_TILL_CANCELED"
        }

        try:
            response = self.session.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["result"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing order: {e}")
            raise
