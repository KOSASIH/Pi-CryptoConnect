import requests
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class APIUtils:
    @staticmethod
    def generate_api_keypair():
        private_key = serialization.generate_private_key(
            algorithm=serialization.RSA(),
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign_request(private_key, method, endpoint, params):
        timestamp = int(pd.Timestamp.now().timestamp() * 1000)
        message = f"{timestamp}{method}{endpoint}"
        if params:
            message += json.dumps(params, separators=(',', ':'))
        signature = private_key.sign(
            message.encode(),
            padding=serialization.pkcs7.PKCS7Options.Default(),
            algorithm=serialization.rsassa.PSS(
                mgf=serialization.rsassa.MGF1(algorithm=hashes.SHA256()),
                salt_length=serialization.rsassa.PSS.MAX_LENGTH
            )
        )
        return timestamp, signature

    @staticmethod
    def make_request(api_key, api_secret, method, endpoint, params=None):
        private_key, public_key = APIUtils.generate_api_keypair()
        timestamp, signature = APIUtils.sign_request(private_key, method, endpoint, params)
        headers = {
            "X-API-KEY": api_key,
            "X-API-SECRET": api_secret,
            "X-API-TIMESTAMP": str(timestamp),
            "X-API-SIGNATURE": signature.hex()
        }
        response = requests.request(method, endpoint, headers=headers, json=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def validate_response(response):
        # Implement response validation logic here
        pass
