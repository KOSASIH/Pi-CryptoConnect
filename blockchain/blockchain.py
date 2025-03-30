import hashlib
import datetime
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index: int, timestamp: datetime.datetime, data: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block.

        Returns:
            str: The SHA-256 hash of the block.
        """
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self) -> Dict:
        """
        Convert the block to a dictionary representation.

        Returns:
            dict: The block as a dictionary.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        """
        Create the genesis block of the blockchain.

        Returns:
            Block: The genesis block.
        """
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self) -> Block:
        """
        Get the latest block in the blockchain.

        Returns:
            Block: The latest block.
        """
        return self.chain[-1]

    def add_block(self, new_block: Block) -> None:
        """
        Add a new block to the blockchain.

        Args:
            new_block (Block): The new block to add.
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
        logging.info(f"Added block: {new_block.to_dict()}")

    def is_valid(self) -> bool:
        """
        Validate the blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                logging.error(f"Invalid hash at block {current_block.index}")
                return False

            # Check if the previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                logging.error(f"Invalid previous hash at block {current_block.index}")
                return False

        logging.info("Blockchain is valid.")
        return True

    def to_dict(self) -> List[Dict]:
        """
        Convert the blockchain to a list of dictionaries.

        Returns:
            list: The blockchain as a list of dictionaries.
        """
        return [block.to_dict() for block in self.chain]

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_block(Block(1, datetime.datetime.now(), "First block after Genesis", blockchain.get_latest_block().hash))
    blockchain.add_block(Block(2, datetime.datetime.now(), "Second block after Genesis", blockchain.get_latest_block().hash))

    # Validate the blockchain
    is_valid = blockchain.is_valid()
    print(f"Blockchain valid: {is_valid}")

    # Print the blockchain
    for block in blockchain.to_dict():
        print(block)
