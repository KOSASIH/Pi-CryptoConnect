from flask import Flask, jsonify, request
import hashlib
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def hash_block(self, index, previous_hash, timestamp, data):
        """Create a SHA-256 hash of a block."""
        block_string = f"{index}{previous_hash}{timestamp}{data}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data):
        """Add a new block to the blockchain."""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        hash_value = self.hash_block(index, previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash_value)
        self.chain.append(new_block)
        return new_block

# Initialize the blockchain
blockchain = Blockchain()

@app.route("/api/create_block", methods=["POST"])
def create_block():
    """
    Create a new block and add it to the blockchain.

    Returns:
        dict: The new block.
    """
    try:
        data = request.json.get("data")
        if not data:
            return jsonify({"error": "Data is required to create a block."}), 400

        new_block = blockchain.add_block(data)
        logging.info(f"New block created: {new_block.to_dict()}")
        return jsonify(new_block.to_dict()), 201

    except Exception as e:
        logging.error(f"Error creating block: {e}")
        return jsonify({"error": "An error occurred while creating the block."}), 500

@app.route("/api/chain", methods=["GET"])
def get_chain():
    """
    Get the full blockchain.

    Returns:
        list: The blockchain.
    """
    chain_data = [block.to_dict() for block in blockchain.chain]
    return jsonify(chain_data), 200

if __name__ == "__main__":
    app.run(debug=True)
