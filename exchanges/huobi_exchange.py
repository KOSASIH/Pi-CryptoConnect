# pi_cryptoconnect/exchanges/huobi_exchange.py

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO)


class HuobiExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.base_url = "https://api.huobi.pro/v1"

    def _get_headers(self) -> Dict[str, str]:
        return {"Api-Key": self.api_key, "Api-Secret-Key": self.api_secret}

    def _handle_response(self, response: requests.Response) -> List[Dict]:
        response.raise_for_status()
        return response.json()

    def get_historical_klines(
        self, symbol: str, interval: str, start_time: int, end_time: int
    ) -> List[Dict]:
        """
                Retrieves historical klines data from Huobi.

                Args:
                    symbol (str): The symbol to retrieve data for.
                    interval (str): The interval of the klines data.
                    start_time (int): The start time of the data range.
                    end_time (int): The end time of the data range.

        Returns:
                    List[Dict]: A list of dictionaries containing the klines data.
        """
        url = f"{self.base_url}/klines"
        params = {
            "symbol": symbol,
            "period": interval,
            "start-time": start_time,
            "end-time": end_time,
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
        Retrieves account information from Huobi.

        Returns:
            Dict: A dictionary containing the account information.
        """
        url = f"{self.base_url}/account"
        headers = self._get_headers()

        try:
            response = self.session.get(url, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching account info: {e}")
            raise

    def place_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> Dict:
        """
        Places an order on Huobi.

        Args:
            symbol (str): The symbol to place the order for.
            side (str): The side of the order (buy or sell).
            quantity (float): The quantity of the order.
            price (float): The price of the order.

        Returns:
            Dict: A dictionary containing the order information.
        """
        url = f"{self.base_url}/order/place"
        params = {
            "symbol": symbol,
            "type": "limit",
            "side": side,
            "amount": quantity,
            "price": price,
        }
        headers = self._get_headers()

        try:
            response = self.session.post(url, json=params, headers=headers)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error placing order: {e}")
            raise
