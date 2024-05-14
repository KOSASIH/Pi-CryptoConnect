# exchanges/kucoin.py
import hashlib
import hmac
import json
import time
from typing import Dict, List

import requests


class KuCoin:
    """KuCoin exchange implementation."""

    BASE_URL = "https://api.kucoin.com"
    API_VERSION = "/api/v1"

    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        """Initialize KuCoin exchange with API credentials."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def _generate_signature(self, method: str, endpoint: str, data: Dict = None) -> str:
        """Generate a signature for a given request."""
        if data is None:
            data = {}

        ts = int(time.time() * 1000)
        query_string = "&".join([f"{k}={v}" for k, v in sorted(data.items())])
        message = f"{method}\n{self.API_VERSION}\n{endpoint}\n{ts}\n{query_string}"
        signature = hmac.new(
            self.api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        return f"{ts}\n{signature}"

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Send a request to the KuCoin API."""
        if data is None:
            data = {}

        signature = self._generate_signature(method, endpoint, data)
        headers = {
            "KC-API-SIGN": signature,
            "KC-API-TIMESTAMP": str(int(time.time() * 1000)),
            "KC-API-KEY": self.api_key,
            "KC-API-PASSPHRASE": self.passphrase,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        url = f"{self.BASE_URL}{self.API_VERSION}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data)
        else:
            raise ValueError("Invalid method. Supported methods: GET, POST.")

        response.raise_for_status()

        return response.json()

    def get_symbols(self) -> List[str]:
        """Get available symbols on KuCoin."""
        endpoint = "/symbols"
        response = self._request("GET", endpoint)
        symbols = [symbol["symbol"] for symbol in response["data"]]

        return symbols
