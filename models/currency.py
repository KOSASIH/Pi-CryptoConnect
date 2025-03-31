from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Currency(db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    exchange_rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Currency('{self.name}', '{self.symbol}', {self.exchange_rate})"

    def convert(self, amount: float, target_currency) -> float:
        """Convert an amount from this currency to the target currency."""
        if not isinstance(target_currency, Currency):
            raise ValueError("target_currency must be an instance of Currency")
        return amount * (target_currency.exchange_rate / self.exchange_rate)

    @classmethod
    def create(cls, name: str, symbol: str, exchange_rate: float):
        """Create a new currency instance and add it to the database."""
        new_currency = cls(name=name, symbol=symbol, exchange_rate=exchange_rate)
        try:
            db.session.add(new_currency)
            db.session.commit()
            return new_currency
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Currency with name '{name}' or symbol '{symbol}' already exists.")

    @classmethod
    def get_all(cls):
        """Retrieve all currencies from the database."""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, currency_id: int):
        """Retrieve a currency by its ID."""
        return cls.query.get(currency_id)

# Example usage
if __name__ == "__main__":
    # Assuming you have a Flask app context
    from flask import Flask

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currencies.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create the database tables

        # Create a new currency
        try:
            usd = Currency.create(name='United States Dollar', symbol='USD', exchange_rate=1.0)
            eur = Currency.create(name='Euro', symbol='EUR', exchange_rate=0.85)

            # Convert 100 USD to EUR
            amount_in_eur = usd.convert(100, eur)
            print(f"100 USD is equivalent to {amount_in_eur:.2f} EUR")

            # Retrieve all currencies
            all_currencies = Currency.get_all()
            print(all_currencies)

        except ValueError as e:
            print(e)
