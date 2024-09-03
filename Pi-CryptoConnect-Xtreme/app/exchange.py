import ccxt

class Exchange:
    def __init__(self):
        self.exchange = ccxt.binance({
            "apiKey": "YOUR_API_KEY",
            "apiSecret": "YOUR_API_SECRET"
        })

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance["total"]

    def place_order(self, market, side, quantity, price):
        self.exchange.place_order(market, side, quantity, price)
