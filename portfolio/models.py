import requests
from pi_cryptoconnect.database import db

class User(db.Model):
    """User  model to manage user authentication and portfolios."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

class Portfolio(db.Model):
    """Portfolio model to manage a collection of assets."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assets = db.relationship('Asset', backref='portfolio', lazy=True)

    def total_value(self):
        """Calculate the total value of the portfolio based on current asset prices."""
        total = 0.0
        for asset in self.assets:
            total += asset.current_value()  # Call the current_value method of Asset
        return total

class Asset(db.Model):
    """Asset model to manage individual cryptocurrency assets."""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # Use Float for fractional quantities
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)

    def current_value(self):
        """Fetch the current market price of the asset and calculate its total value."""
        current_price = self.fetch_current_price()
        return current_price * self.quantity

    def fetch_current_price(self):
        """Fetch the current price of the asset from a market data API."""
        try:
            # Example API call (replace with a real API endpoint)
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={self.symbol}&vs_currencies=usd')
            if response.status_code == 200:
                return response.json().get(self.symbol, {}).get('usd', 0.0)
            else:
                print(f"Error fetching price for {self.symbol}: {response.status_code}")
                return 0.0  # Return 0 if the API call fails
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return 0.0  # Return 0 if the request fails
