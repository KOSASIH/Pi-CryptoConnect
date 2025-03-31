from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import Currency

db = SQLAlchemy()

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    currency = db.relationship('Currency', backref='trades')

    def __repr__(self):
        return f"Trade('{self.user_id}', {self.amount}, {self.price}, '{self.currency.symbol}')"

    def total_value(self) -> float:
        """Calculate the total value of the trade."""
        return self.amount * self.price

    @classmethod
    def create(cls, user_id: int, currency_id: int, amount: float, price: float):
        """Create a new trade instance and add it to the database."""
        new_trade = cls(user_id=user_id, currency_id=currency_id, amount=amount, price=price)
        try:
            db.session.add(new_trade)
            db.session.commit()
            return new_trade
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Failed to create trade. Please check the provided data.")

    @classmethod
    def get_all(cls):
        """Retrieve all trades from the database."""
        return cls.query.all()

    @classmethod
    def get_by_user(cls, user_id: int):
        """Retrieve all trades for a specific user."""
        return cls.query.filter_by(user_id=user_id).all()

# Example usage
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trades.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Create the database tables

        # Example of creating a trade
        try:
            # Assuming you have a user with ID 1 and a currency with ID 1
            trade = Trade.create(user_id=1, currency_id=1, amount=10, price=50000)
            print(f"Trade created: {trade}")

            # Calculate total value of the trade
            print(f"Total value of the trade: {trade.total_value()}")

            # Retrieve all trades
            all_trades = Trade.get_all()
            print(all_trades)

            # Retrieve trades by user
            user_trades = Trade.get_by_user(1)
            print(user_trades)

        except ValueError as e:
            print(e)
