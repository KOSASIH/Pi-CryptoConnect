class Trading:
    def __init__(self, exchange):
        self.exchange = exchange

    def place_order(self, market, side, quantity, price):
        self.exchange.place_order(market, side, quantity, price)

    def get_position(self, market):
        positions = self.exchange.fetch_positions()
        for position in positions:
            if position["market"] == market:
                return position
        return None

    def close_position(self, market):
        position = self.get_position(market)
        if position:
            self.exchange.place_order(market, "SELL" if position["side"] == "BUY" else "BUY", position["quantity"], position["price"])
