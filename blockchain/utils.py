import hashlib
import json
import time
from typing import Any, Dict, List, Optional

def is_valid_public_key(public_key: str) -> bool:
"""
    Check if a public key is valid.

    Args:
        public_key (str): The public key to be validated.

    Returns:
        bool: Whether the public key is valid.
    """
    if len(public_key) != 64:
        return False

    for char in public_key:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False

    return True

def is_valid_private_key(private_key: str) -> bool:
    """
    Check if a private key is valid.

    Args:
        private_key (str): The private key to be validated.

    Returns:
        bool: Whether the private key is valid.
    """
    if len(private_key) != 128:
        return False

    for char in private_key:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False

    return True

def is_valid_signature(signature: str) -> bool:
    """
    Check if a signature is valid.

    Args:
        signature (str): The signature to be validated.

    Returns:
        bool: Whether the signature is valid.
    """
    if len(signature) != 128:
        return False

    for char in signature:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False

    return True

def is_valid_address(address: str) -> bool:
    """
    Check if an address is valid.

    Args:
        address (str): The address to be validated.

    Returns:
        bool: Whether the address is valid.
    """
    if len(address) != 64:
        return False

    for char in address:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False

    return True

def is_valid_block(block: Dict[str, Any]) -> bool:
    """
    Check if a block is valid.

    Args:
        block (Dict[str, Any]): The block to be validated.

    Returns:
        bool: Whether the block is valid.
    """
    if (
        'index' not in block
        or 'timestamp' not in block
        or 'transactions' not in block
        or 'previous_hash' not in block
        or 'hash' not in block
        or 'nonce' not in block
    ):
        return False

    if not all(isinstance(transaction, dict) for transaction in block['transactions']):
        return False

    if not is_valid_hash(block['hash']):
        return False

    if not is_valid_hash(block['previous_hash']):
        return False

    return True

def is_valid_hash(hash: str) -> bool:
    """
    Check if a hash is valid.

    Args:
        hash (str): The hash to be validated.

    Returns:
        bool: Whether the hash is valid.
    """
    if len(hash) != 64:
        return False

    for char in hash:
        if char not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False

    return True

def is_valid_chain(chain: List[Dict[str, Any]]) -> bool:
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

        if not is_valid_block(current_block):
            return False

        if current_block['previous_hash'] != previous_block['hash']:
            return False

    return True

def calculate_hash(index: int, transactions: List[Dict[str, Any]], previous_hash: str, nonce: int) -> str:
    """
    Calculate the hash of a block.

    Args:
        index (int): The index of the block.
        transactions (List[Dict[str, Any]]): The transactions in the block.
        previous_hash (str): The hash of the previous block.
        nonce (int): The nonce of the block.

    Returns:
        str: The hash of the block.
    """
    data = json.dumps(
        {
            'index': index,
            'transactions': transactions,
            'previous_hash': previous_hash,
            'nonce': nonce,
        },
        sort_keys=True,
    ).encode()
    return hashlib.sha256(data).hexdigest()

def mine_block(blockchain: Blockchain, difficulty: int) -> None:
    """
    Mine a new block by solving the Proof of Work problem.

    Args:
        blockchain (Blockchain): The blockchain to be mined.
        difficulty (int): The difficulty of the Proof of Work problem.
    """
    block = blockchain.get_last_block()
    transactions = blockchain.get_pending_transactions()

    nonce = 0
    while True:
        block_hash = calculate_hash(block['index'] + 1, transactions, block['hash'], nonce)
        if block_hash.startswith('0' * difficulty):
            break
        nonce += 1

    blockchain.add_block(
        {
            'index': block['index'] + 1,
            'timestamp': int(time.time()),
            'transactions': transactions,
            'previous_hash': block['hash'],
            'hash': block_hash,
            'nonce': nonce,
        }
    )
