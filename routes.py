from flask import Blueprint, jsonify, request

from services import CurrencyService

currency_blueprint = Blueprint("currency", __name__)


@currency_blueprint.route("/convert", methods=["POST"])
def convert_currency():
    data = request.get_json()
    source_symbol = data["source_symbol"]
    target_symbol = data["target_symbol"]
    amount = data["amount"]

    source_currency = currency_service.get_currency_by_symbol(source_symbol)
    target_currency = currency_service.get_currency_by_symbol(target_symbol)

    if source_currency and target_currency:
        exchange_rate = target_currency.exchange_rate / source_currency.exchange_rate
        converted_amount = amount * exchange_rate
        return jsonify({"converted_amount": converted_amount})
    return jsonify({"error": "Invalid currency symbols"}), 400
