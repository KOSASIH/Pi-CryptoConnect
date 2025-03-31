# models/user.py

import json
import hashlib
from typing import Dict, Optional, List
from config.constants import Currency, UserStatus
from utils.crypto_utils import generate_private_key, generate_public_key

class User:
    """User  model"""
    
    def __init__(self, username: str, password: str, status: UserStatus = UserStatus.INACTIVE):
        self.username = username
        self.password = hash_password(password)  # Store hashed password
        self.status = status
        self.wallet = None
        self.private_key = None
        self.public_key = None

    def generate_wallet(self):
        """Generate a new wallet for the user"""
        self.private_key = generate_private_key()
        self.public_key = generate_public_key(self.private_key)
        self.wallet = {
            'address': self.public_key,
            'balance': 0.0,
            'transactions': []
        }

    def authenticate(self, password: str) -> bool:
        """Authenticate the user with the given password"""
        return self.password == hash_password(password)

    def deposit(self, amount: float) -> None:
        """Deposit an amount into the user's wallet"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.wallet['balance'] += amount
        self.wallet['transactions'].append({
            'type': 'deposit',
            'amount': amount,
            'balance_after': self.wallet['balance']
        })

    def withdraw(self, amount: float) -> None:
        """Withdraw an amount from the user's wallet"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.wallet['balance']:
            raise ValueError("Insufficient balance.")
        self.wallet['balance'] -= amount
        self.wallet['transactions'].append({
            'type': 'withdrawal',
            'amount': amount,
            'balance_after': self.wallet['balance']
        })

    def to_dict(self) -> Dict[str, Optional[str]]:
        """Convert the user object to a dictionary"""
        return {
            'username': self.username,
            'status': self.status.name,
            'wallet': json.dumps(self.wallet),
            'private_key': self.private_key,
            'public_key': self.public_key
        }

def hash_password(password: str) -> str:
    """Hash the given password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage
if __name__ == "__main__":
    user = User(username="john_doe", password="securepassword")
    user.generate_wallet()
    print(user.to_dict())

    # Deposit and withdraw example
    user.deposit(100)
    print(user.to_dict())

    user.withdraw(50)
    print(user.to_dict())
