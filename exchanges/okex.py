# exchanges/okex.py
import hashlib
import hmac
import json
import time
from typing import Dict, List

import requests


class OKEx:
    """OKEx exchange implementation."""

    BASE_URL = "https://www.okex.com/api/v5"

    def __init__(self, api_key: str, api_secret: str, passphrase: str):
        """Initialize OKEx exchange with API credentials."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def _generate_signature(self, method: str, endpoint: str, data: Dict = None) -> str:
        """Generate a signature for a given request."""
        if data is None:
            data = {}

        ts = int(time.time() * 1000)
        query_string = "&".join([f"{k}={v}" for k, v in sorted(data.items())])
        message = f"{ts}\n{method}\n{endpoint}\n{query_string}"
        signature = hmac.new(
            self.api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        return f"{ts}\n{signature}"

    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Send a request to the OKEx API."""
        if data is None:
            data = {}

        signature = self._generate_signature(method, endpoint, data)
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": str(int(time.time() * 1000)),
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
        }

        url = f"{self.BASE_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError("Invalid method. Supported methods: GET, POST.")

        response.raise_for_status()

        return response.json()

    def get_symbols(self) -> List[str]:
        """Get available symbols on OKEx."""
        endpoint = "/spot/markets"
        response = self._request("GET", endpoint)
        symbols = [symbol["instrument_id"] for symbol in response["data"]]

        return symbols
