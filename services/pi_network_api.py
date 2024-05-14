# services/pi_network_api.py

import requests
import json
from typing import Dict, Optional

from config.constants import Currency, Network
from models.user import User

class PiNetworkApi:
    """Pi Network API service"""
    def __init__(self, network: Network = Network.MAINNET):
        self.network = network
        self.api_endpoint = f'https://api.pi.network/{self.network}'

    def get_balance(self, user: User) -> Optional[int]:
        """Get the balance of the user's wallet"""
        response = requests.get(f'{self.api_endpoint}/wallet/{user.wallet["address"]}')
        if response.status_code == 200:
            data = response.json()
            return data.get('balance', 0)
        else:
            print(f'Error getting balance: {response.status_code} {response.reason}')
            return None

    def send_transaction(self, user: User, recipient: str, amount: int) -> bool:
        """Send a transaction from the user's wallet to the recipient"""
        data = {
            'sender': user.wallet["address"],
            'recipient': recipient,
            'amount': amount,
            'currency': Currency.PI.name
        }
        response = requests.post(f'{self.api_endpoint}/transaction', json=data)
        if response.status_code == 201:
            return True
        else:
            print(f'Error sending transaction: {response.status_code} {response.reason}')
            return False

    def get_transaction_history(self, user: User) -> Optional[List[Dict]]:
        """Get the transaction history of the user's wallet"""
        response = requests.get(f'{self.api_endpoint}/wallet/{user.wallet["address"]}/transactions')
        if response.status_code == 200:
            data = response.json()
            return data.get('transactions', [])
        else:
            print(f'Error getting transaction history: {response.status_code} {response.reason}')
            return None
