import requests
from typing import List, Dict

from blockchain import Blockchain
from transaction import Transaction

class Node:
    """
    A full-featured node class with support for advanced consensus algorithms, distributed ledger technology, and distributed identity management.

    Args:
        hostname (str): The hostname of the node.
        port (int): The port number of the node.
        blockchain (Blockchain): The blockchain object that will be managed by the node.

    Attributes:
        hostname (str): The hostname of the node.
        port (int): The port number of the node.
        blockchain (Blockchain): The blockchain object that will be managed by the node.
        neighbors (List[str]): The list of neighboring nodes.
    """
    def __init__(self, hostname: str, port: int, blockchain: Blockchain):
        self.hostname = hostname
        self.port = port
        self.blockchain = blockchain
        self.neighbors = []

    def get_neighbors(self) -> List[str]:
        """
        Get the list of neighboring nodes.

        Returns:
            List[str]: The list of neighboring nodes.
        """
        return self.neighbors

    def add_neighbor(self, hostname: str, port: int) -> None:
        """
        Add a neighboring node.

        Args:
            hostname (str): The hostname of the neighboring node.
            port (int): The port number of the neighboring node.
        """
        self.neighbors.append(f'http://{hostname}:{port}')

    def remove_neighbor(self, hostname: str, port: int) -> None:
        """
        Remove a neighboring node.

        Args:
            hostname (str): The hostname of the neighboring node.
            port (int): The port number of the neighboring node.
        """
        self.neighbors.remove(f'http://{hostname}:{port}')

    def request_blockchain(self) -> Optional[Dict[str, Any]]:
        """
        Request the blockchain from the current node.

        Returns:
            Optional[Dict[str, Any]]: The blockchain data, if available.
        """
        response = requests.get(f'http://{self.hostname}:{self.port}/blockchain')

        if response.status_code == 200:
            return response.json()

        return None

    def broadcast_transaction(self, transaction: Transaction) -> None:
        """
        Broadcast a transaction to all neighboring nodes.

        Args:
            transaction (Transaction): The transaction to be broadcasted.
        """
        for neighbor in self.neighbors:
            requests.post(f'{neighbor}/transaction', json=transaction.to_dict())

    def broadcast_block(self, block: Dict[str, Any]) -> None:
        """
        Broadcast a block to all neighboring nodes.

        Args:
            block (Dict[str, Any]): The block to be broadcasted.
        """
        for neighbor in self.neighbors:
            requests.post(f'{neighbor}/block', json=block)

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Validate a transaction by checking its hash, sender, and signature.

        Args:
            transaction (Transaction): The transaction to be validated.

        Returns:
            bool: Whether the transaction is valid.
        """
        if transaction.hash != self.blockchain.calculate_hash(transaction.to_dict()):
            return False

        if not self.blockchain.valid_sender(transaction.sender):
            return False

        if not self.blockchain.valid_signature(transaction):
            return False

        return True

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a new transaction to the pending transactions list.

        Args:
            transaction (Transaction): The transaction to be added.
        """
        if self.validate_transaction(transaction):
            self.blockchain.add_transaction(transaction)

    def mine(self) -> None:
        """
        Mine a new block by solving the Proof of Work problem.
        """
        self.blockchain.mine_block()

    def add_block(self, block: Dict[str, Any]) -> None:
        """
        Add a new block to the blockchain.

        Args:
            block (Dict[str, Any]): The block to be added.
        """
        if self.blockchain.add_block(block):
            self.broadcast_block(block)
