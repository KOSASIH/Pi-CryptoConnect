import requests
import json
import pandas as pd
from cryptography.hmac import HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Exchange:
    def __init__(self, name, api_key, api_secret, base_url):
        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _generate_signature(self, method, endpoint, params):
        timestamp = int(pd.Timestamp.now().timestamp() * 1000)
        message = f"{timestamp}{method}{endpoint}"
        if params:
            message += json.dumps(params, separators=(',', ':'))
        hmac = HMAC(self.api_secret.encode(), hashes.SHA256(), default_backend())
        hmac.update(message.encode())
        signature = hmac.finalize().hex()
        return timestamp, signature

    def _make_request(self, method, endpoint, params=None):
        timestamp, signature = self._generate_signature(method, endpoint, params)
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "X-MBX-SECRET-KEY": self.api_secret,
            "X-MBX-TIMESTAMP": str(timestamp),
            "X-MBX-SIGNATURE": signature
        }
        response = requests.request(method, self.base_url + endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_markets(self):
        return self._make_request("GET", "/symbols")

    def get_market_data(self, market):
        return self._make_request("GET", f"/symbols/{market}/ticker")

    def place_order(self, market, side, quantity, price):
        params = {
            "symbol": market,
            "side": side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": quantity,
            "price": price
        }
        return self._make_request("POST", "/order", params)

    def get_order_book(self, market):
        return self._make_request("GET", f"/symbols/{market}/orderBook")

class BinanceExchange(Exchange):
    def __init__(self, api_key, api_secret):
        super().__init__("Binance", api_key, api_secret, "https://api.binance.com/api/v3")

class CoinbaseExchange(Exchange):
    def __init__(self, api_key, api_secret):
        super().__init__("Coinbase", api_key, api_secret, "https://api.coinbase.com/v2")

    def _generate_signature(self, method, endpoint, params):
        timestamp = int(pd.Timestamp.now().timestamp() * 1000)
        message = f"{timestamp}{method}{endpoint}"
        if params:
            message += json.dumps(params, separators=(',', ':'))
        hmac = HMAC(self.api_secret.encode(), hashes.SHA256(), default_backend())
        hmac.update(message.encode())
        signature = hmac.finalize().hex()
        return timestamp, signature

    def _make_request(self, method, endpoint, params=None):
        timestamp, signature = self._generate_signature(method, endpoint, params)
        headers = {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": str(timestamp),
            "CB-ACCESS-PASSPHRASE": "my_passphrase"
        }
        response = requests.request(method, self.base_url + endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()
