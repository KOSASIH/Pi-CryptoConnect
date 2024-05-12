# core/crypto_connector.py
import hashlib
import hmac
import json
from datetime import datetime
from typing import Optional

import requests


class CryptoConnector:
    def __init__(
        self, api_key: str, api_secret: str, base_url: str = "https://api.example.com"
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _get_signature(self, message: str) -> str:
        return hmac.new(
            self.api_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

    def _request(
        self, method: str, endpoint: str, params: Optional[dict] = None
    ) -> dict:
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
            "Timestamp": datetime.utcnow().isoformat(),
        }
        if params:
            headers["Signature"] = self._get_signature(json.dumps(params))

        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    def get_cryptocurrency_price(self, symbol: str) -> dict:
        endpoint = f"prices/{symbol}"
        return self._request("GET", endpoint)

    def get_cryptocurrencies_prices(self, symbols: List[str]) -> dict:
        endpoint = "prices"
        params = {"symbols": ",".join(symbols)}
        return self._request("GET", endpoint, params=params)
