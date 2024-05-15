import requests

class CryptocurrencyApi:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3/simple/price"
        self.headers = {"Accepts": "application/json"}

    def _get_price(self, symbol: str, currency: str = "usd") -> float:
        url = f"{self.base_url}?ids={symbol}&vs_currencies={currency}"
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data[symbol][currency]

    def fetch_price(self, symbol: str) -> float:
        """Fetch the current price for a given cryptocurrency symbol."""
        return self._get_price(symbol)

    def fetch_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Fetch the current prices for a list of cryptocurrency symbols."""
        prices = {}
        for symbol in symbols:
            prices[symbol] = self._get_price(symbol)
        return prices
