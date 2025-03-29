from typing import Dict, List, Optional, Any
import requests
import logging
from transaction import Transaction
from blockchain import Blockchain

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        consensus_algorithm (str): The consensus algorithm used by the node.
    """

    def __init__(self, hostname: str, port: int, blockchain: Blockchain, consensus_algorithm: str = "Proof of Work"):
        self.hostname = hostname
        self.port = port
        self.blockchain = blockchain
        self.neighbors = []
        self.consensus_algorithm = consensus_algorithm

    def get_neighbors(self) -> List[str]:
        """Get the list of neighboring nodes."""
        return self.neighbors

    def add_neighbor(self, hostname: str, port: int) -> None:
        """Add a neighboring node."""
        self.neighbors.append(f"http://{hostname}:{port}")
        logging.info(f"Added neighbor: {hostname}:{port}")

    def remove_neighbor(self, hostname: str, port: int) -> None:
        """Remove a neighboring node."""
        self.neighbors.remove(f"http://{hostname}:{port}")
        logging.info(f"Removed neighbor: {hostname}:{port}")

    def request_blockchain(self) -> Optional[Dict[str, Any]]:
        """Request the blockchain from the current node."""
        try:
            response = requests.get(f"http://{self.hostname}:{self.port}/blockchain")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error requesting blockchain: {e}")
            return None

    def broadcast_transaction(self, transaction: Transaction) -> None:
        """Broadcast a transaction to all neighboring nodes."""
        for neighbor in self.neighbors:
            try:
                response = requests.post(f"{neighbor}/transaction", json=transaction.to_dict())
                response.raise_for_status()
                logging.info(f"Broadcasted transaction to {neighbor}")
            except requests.RequestException as e:
                logging.error(f"Error broadcasting transaction to {neighbor}: {e}")

    def broadcast_block(self, block: Dict[str, Any]) -> None:
        """Broadcast a block to all neighboring nodes."""
        for neighbor in self.neighbors:
            try:
                response = requests.post(f"{neighbor}/block", json=block)
                response.raise_for_status()
                logging.info(f"Broadcasted block to {neighbor}")
            except requests.RequestException as e:
                logging.error(f"Error broadcasting block to {neighbor}: {e}")

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction by checking its hash, sender, and signature."""
        if transaction.hash != self.blockchain.calculate_hash(transaction.to_dict()):
            logging.warning("Invalid transaction hash.")
            return False

        if not self.blockchain.valid_sender(transaction.sender):
            logging.warning("Invalid transaction sender.")
            return False

        if not self.blockchain.valid_signature(transaction):
            logging.warning("Invalid transaction signature.")
            return False

        return True

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to the pending transactions list."""
        if self.validate_transaction(transaction):
            self.blockchain.add_transaction(transaction)
            logging.info(f"Transaction added: {transaction.hash}")
        else:
            logging.warning(f"Transaction validation failed: {transaction.hash}")

    def mine(self) -> None:
        """Mine a new block by solving the Proof of Work problem."""
        if self.cons ensus_algorithm == "Proof of Work":
            self.blockchain.mine_block()
            logging.info("New block mined.")
        else:
            logging.warning("Mining not supported for the current consensus algorithm.")

    def add_block(self, block: Dict[str, Any]) -> None:
        """Add a new block to the blockchain."""
        if self.blockchain.add_block(block):
            self.broadcast_block(block)
            logging.info(f"Block added to the blockchain: {block['hash']}")
        else:
            logging.warning("Failed to add block to the blockchain.")

    def health_check(self) -> None:
        """Check the health of neighboring nodes."""
        for neighbor in self.neighbors:
            try:
                response = requests.get(f"{neighbor}/health")
                if response.status_code == 200:
                    logging.info(f"Neighbor {neighbor} is healthy.")
                else:
                    logging.warning(f"Neighbor {neighbor} is not healthy.")
            except requests.RequestException as e:
                logging.error(f"Error checking health of {neighbor}: {e}")

    def configure_node(self, consensus_algorithm: str) -> None:
        """Dynamically configure the node's consensus algorithm."""
        self.consensus_algorithm = consensus_algorithm
        logging.info(f"Consensus algorithm set to: {self.consensus_algorithm}")

    def manage_transaction_pool(self) -> List[Transaction]:
        """Manage a pool of pending transactions with prioritization."""
        # Placeholder for transaction pool management logic
        return self.blockchain.get_pending_transactions()
