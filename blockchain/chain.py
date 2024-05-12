import hashlib
import json
import time
from typing import Any, Dict, List, Optional

from node import Node
from transaction import Transaction

class Blockchain:
    """
    A full-featured blockchain class with support for advanced consensus algorithms, distributed ledger technology, and distributed identity management.

    Args:
        node (Node): The node object that will be used to manage the blockchain.
        consensus_algorithm (str): The consensus algorithm to be used by the blockchain.
        distributed_ledger (bool): Whether the blockchain should use a distributed ledger technology.
        distributed_identity (bool): Whether the blockchain should use a distributed identity management system.

    Attributes:
        node (Node): The node object that will be used to manage the blockchain.
        consensus_algorithm (str): The consensus algorithm to be used by the blockchain.
        distributed_ledger (bool): Whether the blockchain should use a distributed ledger technology.
        distributed_identity (bool): Whether the blockchain should use a distributed identity management system.
        chain (List[Dict[str, Any]]): The list of blocks in the blockchain.
        pending_transactions (List[Transaction]): The list of pending transactions.
    """
    def __init__(
        self,
        node: Node,
        consensus_algorithm: str,
        distributed_ledger: bool = False,
        distributed_identity: bool = False,
    ):
        self.node = node
        self.consensus_algorithm = consensus_algorithm
        self.distributed_ledger = distributed_ledger
        self.distributed_identity = distributed_identity
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self) -> Dict[str, Any]:
        """
        Create the genesis block for the blockchain.

        Returns:
            dict: The genesis block.
        """
        return {
            'index': 0,
            'timestamp': int(time.time()),
            'transactions': [],
            'previous_hash': '0' * 64,
            'hash': self.calculate_hash(0, [], '0' * 64),
            'nonce': 0,
        }

    def calculate_hash(self, index: int, transactions: List[Transaction], previous_hash: str) -> str:
        """
        Calculate the hash of a block.

        Args:
            index (int): The index of the block.
            transactions (List[Transaction]): The list of transactions in the block.
            previous_hash (str): The hash of the previous block.

        Returns:
            str: The hash of the block.
        """
        data = json.dumps(
            {
                'index': index,
                'transactions': transactions,
                'previous_hash': previous_hash,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(data).hexdigest()

    def add_block(self) -> None:
        """
        Add a new block to the blockchain.
        """
        if self.pending_transactions:
            block = {
                'index': len(self.chain),
                'timestamp': int(time.time()),
                'transactions': self.pending_transactions,
                'previous_hash': self.chain[-1]['hash'],
                'nonce': 0,
            }
            self.pending_transactions = []
            while not self.is_block_valid(block):
                block['nonce'] += 1
            block['hash'] = self.calculate_hash(block['index'], block['transactions'], block['previous_hash'])
            self.chain.append(block)

    def is_block_valid(self, block: Dict[str, Any]) -> bool:
        """
        Check if a block is valid.

        Args:
            block (Dict[str, Any]): The block to be validated.

        Returns:
            bool: Whether the block is valid.
        """
        if (
            block['index'] != len(self.chain)
            or block['previous_hash'] != self.chain[-1]['hash']
            or block['hash'] != self.calculate_hash(block['index'], block['transactions'], block['previous_hash'])
        ):
            return False
        return True

    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a new transaction to the pending transactions list.

        Args:
            transaction (Transaction): The transaction to be added.
        """
        self.pending_transactions.append(transaction)

    def is_chain_valid(self) -> bool:
        """
        Check if the blockchain is valid.

        Returns:
            bool: Whether the blockchain is valid.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block['hash'] != self.calculate_hash(
                current_block['index'],
                current_block['transactions'],
                previous_block['hash'],
            ):
                return False
        return True

    def resolve_conflicts(self) -> Optional[bool]:
        """
        Resolve conflicts in the blockchain by adopting the longest chain.

        Returns:
            Optional[bool]: Whether the conflicts were resolved.
        """
        neighbors = self.node.get_neighbors()
        new_chain = None

        max_length = len(self.chain)

        for neighbor in neighbors:
            response = neighbor.request_blockchain()

            if response is None:
                continue

            length = response['length']
            chain = response['chain']

            if length > max_length and self.chain_is_valid(chain):
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def chain_is_valid(self, chain: List[Dict[str, Any]]) -> bool:
        """
        Check if a chain is valid.

        Args:
            chain (List[Dict[str, Any]]): The chain to be validated.

        Returns:
            bool: Whether the chain is valid.
        """
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            if current_block['hash'] != self.calculate_hash(
                current_block['index'],
                current_block['transactions'],
                previous_block['hash'],
            ):
                return False
        return True
