import requests
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app.exchange import Exchange
from app.trading import Trading

app = Flask(__name__)
api = Api(app)

class API(Resource):
    def get(self):
        return {"message": "Welcome to the API"}

    def post(self):
        data = request.get_json()
        if data["action"] == "place_order":
            exchange = Exchange()
            trading = Trading(exchange)
            trading.place_order(data["market"], data["side"], data["quantity"], data["price"])
            return {"message": "Order placed successfully"}
        elif data["action"] == "get_balance":
            exchange = Exchange()
            balance = exchange.get_balance()
            return {"balance": balance}
        else:
            return {"message": "Invalid action"}

api.add_resource(API, "/api")

if __name__ == "__main__":
    app.run(debug=True)
