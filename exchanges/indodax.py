# exchanges/indodax.py
import ccxt


class Indodax:
    """Indodax exchange implementation."""

    def __init__(self):
        """Initialize Indodax exchange."""
        self.exchange = ccxt.indodax()

    def get_symbols(self) -> List[str]:
        """Get available symbols on Indodax."""
        symbols = self.exchange.load_markets()
        return list(symbols.keys())
