from services import CurrencyService

currency_service = CurrencyService()


def execute_trade(user_id, amount, price, currency_symbol):
    currency = currency_service.get_currency_by_symbol(currency_symbol)
    if currency:
        trade = Trade(
            user_id=user_id, amount=amount, price=price, currency_id=currency.id
        )
        db.session.add(trade)
        db.session.commit()
        return True
    return False
