import hashlib
import secrets
import time
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_block(index: int, previous_hash: str, transactions: List[Dict[str, str]]) -> Dict:
    """
    Create a new block and add it to the blockchain.

    Args:
        index (int): The index of the new block.
        previous_hash (str): The hash of the previous block.
        transactions (list): A list of transactions to be included in the block.

    Returns:
        dict: The new block.
    """
    timestamp = time.time()
    block_data = {
        "index": index,
        "previous_hash": previous_hash,
        "timestamp": timestamp,
        "transactions": transactions
    }
    block_hash = hash_block(block_data)
    block_data["hash"] = block_hash
    logging.info(f"Created block: {block_data}")
    return block_data

def hash_block(block: Dict) -> str:
    """
    Create a SHA-256 hash of a block.

    Args:
        block (dict): The block to hash.

    Returns:
        str: The SHA-256 hash of the block.
    """
    block_string = f"{block['index']}{block['previous_hash']}{block['timestamp']}{block['transactions']}".encode()
    return hashlib.sha256(block_string).hexdigest()

def generate_private_key() -> str:
    """
    Generate a secure private key.

    Returns:
        str: The generated private key.
    """
    private_key = secrets.token_hex(32)
    logging.info(f"Generated private key: {private_key}")
    return private_key

# Example usage
if __name__ == "__main__":
    # Create a genesis block
    genesis_block = create_block(0, "0", [{"sender": "Alice", "recipient": "Bob", "amount": 10}])
    print(genesis_block)

    # Generate a private key
    private_key = generate_private_key()
    print(f"Private Key: {private_key}")
