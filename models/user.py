# models/user.py

import hashlib
import json
from typing import Dict, Optional

from config.constants import Currency, UserStatus
from utils.crypto_utils import generate_private_key, generate_public_key


class User:
    """User model"""

    def __init__(
        self, username: str, password: str, status: UserStatus = UserStatus.INACTIVE
    ):
        self.username = username
        self.password = password
        self.status = status
        self.wallet = None
        self.private_key = None
        self.public_key = None

    def generate_wallet(self):
        """Generate a new wallet for the user"""
        self.private_key = generate_private_key()
        self.public_key = generate_public_key(self.private_key)
        self.wallet = {"address": self.public_key, "balance": 0, "transactions": []}

    def authenticate(self, password: str) -> bool:
        """Authenticate the user with the given password"""
        return self.password == hash_password(password)

    def to_dict(self) -> Dict[str, str]:
        """Convert the user object to a dictionary"""
        return {
            "username": self.username,
            "status": self.status.name,
            "wallet": json.dumps(self.wallet),
            "private_key": self.private_key,
            "public_key": self.public_key,
        }


def hash_password(password: str) -> str:
    """Hash the given password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()
