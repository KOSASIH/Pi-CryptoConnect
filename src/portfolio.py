# src/portfolio.py

import json
from datetime import datetime

class Transaction:
    def __init__(self, currency, amount, transaction_type):
        self.currency = currency
        self.amount = amount
        self.transaction_type = transaction_type  # 'buy' or 'sell'
        self.timestamp = datetime.now().isoformat()  # Record the time of the transaction

    def __str__(self):
        return f"{self.transaction_type.capitalize()} {self.amount} of {self.currency} on {self.timestamp}"

class Portfolio:
    def __init__(self):
        self.portfolio = {}  # Dictionary to hold currency and amount
        self.transactions = []  # List to hold transaction history

    def add_currency(self, currency, amount):
        """Add a currency to the portfolio."""
        if currency in self.portfolio:
            self.portfolio[currency] += amount
        else:
            self.portfolio[currency] = amount
        self.transactions.append(Transaction(currency, amount, 'buy'))

    def remove_currency(self, currency, amount):
        """Remove a currency from the portfolio."""
        if currency in self.portfolio and self.portfolio[currency] >= amount:
            self.portfolio[currency] -= amount
            if self.portfolio[currency] == 0:
                del self.portfolio[currency]
            self.transactions.append(Transaction(currency, amount, 'sell'))
            return f"Removed {amount} of {currency} from portfolio."
        return "Insufficient amount or currency not found."

    def view_portfolio(self):
        """View the current portfolio."""
        if not self.portfolio:
            return "Your portfolio is empty."
        return "\n".join(f"{currency}: {amount}" for currency, amount in self.portfolio.items())

    def view_transactions(self):
        """View the transaction history."""
        if not self.transactions:
            return "No transactions found."
        return "\n".join(str(transaction) for transaction in self.transactions)

    def save_portfolio(self, username):
        """Save the portfolio and transactions to a JSON file."""
        data = {
            'portfolio': self.portfolio,
            'transactions': [str(tx) for tx in self.transactions]
        }
        with open(f"{username}_portfolio.json", 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_portfolio(username):
        """Load the portfolio and transactions from a JSON file."""
        try:
            with open(f"{username}_portfolio.json", 'r') as f:
                data = json.load(f)
                portfolio = Portfolio()
                portfolio.portfolio = data['portfolio']
                portfolio.transactions = [Transaction(tx['currency'], tx['amount'], tx['transaction_type']) for tx in data['transactions']]
                return portfolio
        except FileNotFoundError:
            return Portfolio()  # Return an empty portfolio if the file does not exist
