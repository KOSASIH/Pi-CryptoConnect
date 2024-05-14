# exchanges/fantasy_exchange.py
class FantasyExchange:
    """Fantasy exchange implementation."""

    def __init__(self):
        """Initialize FantasyExchange."""
        self.symbols = {}

    def add_symbol(self, symbol: str, price: float):
        """Add a new symbol to the FantasyExchange."""
        self.symbols[symbol] = price

    def get_symbols(self) -> List[str]:
        """Get available symbols on FantasyExchange."""
        return list(self.symbols.keys())

    def get_price(self, symbol: str) -> float:
        """Get the price of a specific symbol on FantasyExchange."""
        return self.symbols[symbol]

    def update_price(self, symbol: str, price: float):
        """Update the price of a specific symbol on FantasyExchange."""
        self.symbols[symbol] = price
