import unittest
from src.cryptocurrency_api import CryptocurrencyApi

class TestCryptocurrencyApi(unittest.TestCase):
    def setUp(self):
        self.api = CryptocurrencyApi()

    def test_fetch_price(self):
        price = self.api.fetch_price("bitcoin")
        self.assertGreater(price, 0)

    def test_fetch_prices(self):
        prices = self.api.fetch_prices(["bitcoin", "ethereum"])
        self.assertGreater(len(prices), 0)
        self.assertIn("bitcoin", prices)
        self.assertIn("ethereum", prices)
        self.assertGreater(prices["bitcoin"], 0)
        self.assertGreater(prices["ethereum"], 0)

if __name__ == "__main__":
    unittest.main()
