# core/data_processor.py
from typing import List, Dict
from .models import CryptoCurrency

class DataProcessor:
    @staticmethod
    def process_cryptocurrency_prices(prices: List[Dict[str, float]]) -> List[CryptoCurrency]:
        return [
            CryptoCurrency(
                name=price["name"],
                symbol=price["symbol"],
                price=price["price"],
            )
            for price in prices
        ]

    @staticmethod
    def process_cryptocurrencies_prices(prices: Dict[str, Dict[str, float]]) -> List[CryptoCurrency]:
        return [
            CryptoCurrency(
                name=price["name"],
                symbol=price["symbol"],
                price=price["price"],
            )
            for symbol, price in prices.items()
        ]
