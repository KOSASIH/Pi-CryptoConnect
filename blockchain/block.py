# Use type hints and docstrings for better code readability
import secrets


def create_block(index: int, previous_hash: str, transactions: list) -> dict:
    """
    Create a new block and add it to the blockchain.

    Args:
        index (int): The index of the new block.
        previous_hash (str): The hash of the previous block.
        transactions (list): A list of transactions to be included in the block.

    Returns:
        dict: The new block.
    """
    # ...


# Use a more secure random number generator


def generate_private_key() -> str:
    """
    Generate a secure private key.

    Returns:
        str: The generated private key.
    """
    return secrets.token_hex(32)
