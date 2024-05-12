from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/api/create_block", methods=["POST"])
def create_block():
    """
    Create a new block and add it to the blockchain.

    Returns:
        dict: The new block.
    """
    # ...


if __name__ == "__main__":
    app.run(debug=True)
