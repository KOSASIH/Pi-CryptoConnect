from models import Currency


class CurrencyService:
    def get_all_currencies(self):
        return Currency.query.all()

    def get_currency_by_id(self, currency_id):
        return Currency.query.get(currency_id)

    def get_currency_by_symbol(self, symbol):
        return Currency.query.filter_by(symbol=symbol).first()

    def update_exchange_rate(self, currency_id, new_exchange_rate):
        currency = self.get_currency_by_id(currency_id)
        if currency:
            currency.exchange_rate = new_exchange_rate
            db.session.commit()
            return True
        return False
