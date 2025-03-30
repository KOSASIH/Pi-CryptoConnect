from flask import Blueprint, request, jsonify
from services import CurrencyService
from flask_caching import Cache
import logging
import os
from marshmallow import Schema, fields, ValidationError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

currency_blueprint = Blueprint('currency', __name__)
currency_service = CurrencyService()

# Define a schema for input validation
class CurrencyConversionSchema(Schema):
    source_symbol = fields.Str(required=True)
    target_symbol = fields.Str(required=True)
    amount = fields.Float(required=True)

@currency_blueprint.route('/convert', methods=['POST'])
@cache.cached(timeout=60, query_string=True)  # Cache the response for 60 seconds
async def convert_currency():
    # Validate input data
    schema = CurrencyConversionSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify({'error': 'Invalid input', 'details': err.messages}), 400

    source_symbol = data['source_symbol']
    target_symbol = data['target_symbol']
    amount = data['amount']

    try:
        source_currency = currency_service.get_currency_by_symbol(source_symbol)
        target_currency = currency_service.get_currency_by_symbol(target_symbol)

        if source_currency and target_currency:
            exchange_rate = target_currency.exchange_rate / source_currency.exchange_rate
            converted_amount = amount * exchange_rate
            logger.info(f"Converted {amount} {source_symbol} to {converted_amount} {target_symbol}")
            return jsonify({'converted_amount': converted_amount})
        
        logger.warning(f"Invalid currency symbols: {source_symbol}, {target_symbol}")
        return jsonify({'error': 'Invalid currency symbols'}), 400

    except Exception as e:
        logger.exception("An error occurred during currency conversion")
        return jsonify({'error': 'Internal server error'}), 500

# Ensure to run the app with the correct configuration
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(currency_blueprint)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
