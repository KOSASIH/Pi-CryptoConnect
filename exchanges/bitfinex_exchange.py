# pi_cryptoconnect/bitfinex_exchange.py

import logging
import requests
import hmac
import hashlib
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class BitfinexExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.base_url = "https://api.bitfinex.com/v2"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-BFX-APIKEY": self.api_key
        }

    def _generate_signature(self, url: str, data: Dict) -> str:
        message = f"{url}?{self._encode_data(data)}".encode()
        signature = hmac.new(self.api_secret.encode(), message, hashlib.sha384).hexdigest()
        return signature

    def _encode_data(self, data: Dict) -> str:
        return "&".join([f"{k}={v}" for k, v in sorted(data.items())])

    def _handle_response(self, response: requests.Response) -> List[Dict]:
        response.raise_for_status()
        return response.json()

    def get_historical_klines(self, symbol: str, interval: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Retrieves historical klines data from Bitfinex.

        Args:
            symbol (str): The symbol to fetch the klines data for.
            interval (str): The interval of the klines data.
            start_time (int): The start time of the data range.
            end_time (int): The end time of the data range.

        Returns:
            List[Dict]: A list of dictionaries containing the klines data.
        """
        url = f"{self.base_url}/candles/trade:{symbol}:{interval}"
        data = {
            "end": end_time,
            "limit": 1000,
            "start": start_time
        }
        headers = self._get_headers()
        signature = self._generate_signature(url, data)

        try:
            response = self.session.get(url, params=data, headers={**headers, "X-BFX-SIGNATURE": signature})
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def get_account_info(self) -> Dict:
        """
        Retrieves account information from Bitfinex.

        Returns:
            Dict: A dictionary containing the account information.
        """
        url = f"{self.base_url}/auth/r/wallets"
        headers = self._get_headers()

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def place_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """
        Places an order on Bitfinex.

        Args:
            symbol (str): The symbol to place the order for.
            side (str): The side of the order (buy or sell).
            quantity (float): The quantity of the order.
            price (float): The price of the order.

        Returns:
            Dict: A dictionary containing the order information.
        """
        url = f"{self.base_url}/auth/r/orders"
        headers = self._get_headers()
        data = {
            "symbol": symbol,
            "amount": str(quantity),
            "price": str(price),
            "side": side,
            "type": "EXCHANGE LIMIT"
        }
        signature = self._generate_signature(url, data)

        try:
           response = self.session.post(url, json=data, headers={**headers, "X-BFX-SIGNATURE": signature})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing order: {e}")
            raise
