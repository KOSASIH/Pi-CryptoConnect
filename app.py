from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

@app.route('/crypto', methods=['POST'])
def add_crypto():
    data = request.get_json()
    name = data['name']
    price = data['price']
    new_crypto = Crypto(name, price)
    db.session.add(new_crypto)
    db.session.commit()
    return jsonify({'message': 'Crypto added successfully'})

@app.route('/crypto', methods=['GET'])
def get_crypto():
    all_crypto = Crypto.query.all()
    output = []
    for crypto in all_crypto:
        crypto_data = {'id': crypto.id, 'name': crypto.name, 'price': crypto.price}
        output.append(crypto_data)
    return jsonify({'result': output})

@app.route('/crypto/<id>', methods=['PUT'])
def update_crypto(id):
    data = request.get_json()
    crypto = Crypto.query.get(id)
    crypto.name = data['name']
    crypto.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Crypto updated successfully'})

@app.route('/crypto/<id>', methods=['DELETE'])
def delete_crypto(id):
    crypto = Crypto.query.get(id)
    db.session.delete(crypto)
    db.session.commit()
    return jsonify({'message': 'Crypto deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
