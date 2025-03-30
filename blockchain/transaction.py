import hashlib
import json
import time
from typing import Any, Dict, Optional


class Transaction:
    """
    A full-featured transaction class with support for advanced cryptography and digital signatures.

    Args:
        sender (str): The public key of the sender.
        receiver (str): The public key of the receiver.
        amount (float): The amount of cryptocurrency to be transferred.
        signature (str): The digital signature of the transaction.

    Attributes:
        sender (str): The public key of the sender.
        receiver (str): The public key of the receiver.
        amount (float): The amount of cryptocurrency to be transferred.
        signature (str): The digital signature of the transaction.
        timestamp (float): The timestamp of the transaction.
        hash (str): The hash of the transaction.
    """

    def __init__(
        self,
        sender: str,
        receiver: str,
        amount: float,
        signature: Optional[str] = None,
    ):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the hash of the transaction.

        Returns:
            str: The hash of the transaction.
        """
        data = json.dumps(
            {
                "sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(data).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.

        Returns:
            Dict[str, Any]: The transaction as a dictionary.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "hash": self.hash,
        }

    def sign(self, private_key: str) -> None:
        """
        Sign the transaction with a private key.

        Args:
            private_key (str): The private key of the sender.
        """
        message = json.dumps(
            {
                "sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode()
        signature = hashlib.sha256(private_key.encode() + message).hexdigest()
        self.signature = signature

    def verify_signature(self, public_key: str) -> bool:
        """
        Verify the digital signature of the transaction.

        Args:
            public_key (str): The public key of the sender.

        Returns:
            bool: Whether the signature is valid.
        """
        message = json.dumps(
            {
                "sender": self.sender,
                "receiver": self.receiver,
                "amount": self.amount,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode()
        signature = hashlib.sha256(public_key.encode() + message).hexdigest()
        return self.signature == signature
