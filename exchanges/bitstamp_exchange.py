# pi_cryptoconnect/bitstamp_exchange.py

import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

class BitstampExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.base_url = "https://www.bitstamp.net/api"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def _handle_response(self, response: requests.Response) -> List[Dict]:
        response.raise_for_status()
        return response.json()["data"]

    def get_historical_klines(self, symbol: str, interval: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Retrieves historical klines data from Bitstamp.

        Args:
            symbol (str): The symbol to fetch the klines data for.
            interval (str): The interval of the klines data.
            start_time (int): The start time of the data range.
            end_time (int): The end time of the data range.

        Returns:
            List[Dict]: A list of dictionaries containing the klines data.
        """
        url = f"{self.base_url}/ticker/{symbol}"
        params = {
            "period": interval,
            "start": start_time,
            "end": end_time
        }
        headers = self._get_headers()

        try:
            response = self.session.get(url, params=params, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def get_account_info(self) -> Dict:
        """
        Retrieves account information from Bitstamp.

        Returns:
            Dict: A dictionary containing the account information.
        """
        url = f"{self.base_url}/balance/"
        headers = self._get_headers()
        headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["balance"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def place_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """
        Places an order on Bitstamp.

        Args:
            symbol (str): The symbol to place the order for.
            side (str): The side of the order (buy or sell).
            quantity (float): The quantity of the order.
            price (float): The price of the order.

        Returns:
            Dict: A dictionary containing the order information.
        """
        url = f"{self.base_url}/order/"
        headers = self._get_headers()
        headers["Authorization"] = f"Bearer {self.api_key}"
        data = {
            "amount": str(quantity),
            "price": str(price),
            "symbol": symbol,
            "type": "limit" if side == "buy" else "limit_sell"
        }

        try:
            response = self.session.post(url, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing order: {e}")
            raise
