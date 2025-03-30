import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Crypto model
class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

# Define the schema for validation
class CryptoSchema(Schema):
    name = fields.String(required=True)
    price = fields.Float(required=True)

crypto_schema = CryptoSchema()
cryptos_schema = CryptoSchema(many=True)

@app.route('/crypto', methods=['POST'])
def add_crypto():
    try:
        data = request.get_json()
        crypto_data = crypto_schema.load(data)  # Validate and deserialize input
        new_crypto = Crypto(**crypto_data)
        db.session.add(new_crypto)
        db.session.commit()
        return jsonify({'message': 'Crypto added successfully', 'id': new_crypto.id}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        logging.error(f"Error adding crypto: {e}")
        return jsonify({'message': 'An error occurred while adding crypto'}), 500

@app.route('/crypto', methods=['GET'])
def get_crypto():
    try:
        all_crypto = Crypto.query.all()
        output = cryptos_schema.dump(all_crypto)  # Serialize output
        return jsonify({'result': output}), 200
    except Exception as e:
        logging.error(f"Error retrieving crypto: {e}")
        return jsonify({'message': 'An error occurred while retrieving crypto'}), 500

@app.route('/crypto/<int:id>', methods=['PUT'])
def update_crypto(id):
    try:
        data = request.get_json()
        crypto = Crypto.query.get_or_404(id)  # Automatically returns 404 if not found
        crypto_data = crypto_schema.load(data)  # Validate and deserialize input
        crypto.name = crypto_data['name']
        crypto.price = crypto_data['price']
        db.session.commit()
        return jsonify({'message': 'Crypto updated successfully'}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        logging.error(f"Error updating crypto: {e}")
        return jsonify({'message': 'An error occurred while updating crypto'}), 500

@app.route('/crypto/<int:id>', methods=['DELETE'])
def delete_crypto(id):
    try:
        crypto = Crypto.query.get_or_404(id)  # Automatically returns 404 if not found
        db.session.delete(crypto)
        db.session.commit()
        return jsonify({'message': 'Crypto deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting crypto: {e}")
        return jsonify({'message': 'An error occurred while deleting crypto'}), 500

if __name__ == '__main__':
    app.run(debug=True)
