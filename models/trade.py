from models import Currency


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.id"))
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    currency = db.relationship("Currency", backref="trades")

    def __repr__(self):
        return f"Trade('{self.user_id}', {self.amount}, {self.price}, {self.currency.symbol})"
