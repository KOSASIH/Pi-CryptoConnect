# pi_cryptoconnect/exchanges/binance_exchange.py

import logging
import requests
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

class BinanceExchange:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    def get_historical_klines(self, symbol: str, interval: str, start_time: int, end_time: int) -> List[Dict]:
        """
        Retrieves historical klines data from Binance.

        Args:
            symbol (str): The symbol to retrieve data for.
            interval (str): The interval of the klines data.
            start_time (int): The start time of the data range.
            end_time (int): The end time of the data range.

        Returns:
            List[Dict]: A list of dictionaries containing the klines data.
        """
        if not isinstance(symbol, str) or not symbol.isalpha():
            raise ValueError("Invalid symbol")

        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data:{e}")
            raise

        return response.json()
