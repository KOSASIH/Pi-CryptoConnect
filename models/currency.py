from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Currency('{self.name}', '{self.symbol}', {self.exchange_rate})"
