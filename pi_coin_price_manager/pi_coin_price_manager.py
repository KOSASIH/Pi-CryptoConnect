import time
from exchanges.okex import OKEx
from exchanges.indodax import Indodax

# Initialize exchange instances with API credentials
okex = OKEx("YOUR_API_KEY", "YOUR_API_SECRET", "YOUR_PASSPHRASE")
indodax = Indodax("YOUR_API_KEY", "YOUR_API_SECRET")

# List of exchanges
exchanges = [okex, indodax]

# Function to update Pi Coin price
def update_pi_coin_price(exchanges: List[Indodax or OKEx]):
    pi_coin_symbol = "PI_USDT"  # Replace with the actual Pi Coin symbol on each exchange

    for exchange in exchanges:
        try:
            # Get the current price of Pi Coin
            current_price = exchange.get_price(pi_coin_symbol)

            # Set the new price of Pi Coin
            if current_price != 314.159:
                exchange.set_price(pi_coin_symbol, 314.159)

            print(f"Updated Pi Coin price on {exchange.__class__.__name__} to $314.159")

        except Exception as e:
            print(f"Error updating Pi Coin price on {exchange.__class__.__name__}: {e}")

# Function to set the price
def set_price(exchange: Indodax or OKEx, symbol: str, price: float):
    # Implement the set_price method for each exchange
    # For example, OKEx and Indodax may have different methods for setting the price
    pass

# Schedule the function to run periodically
while True:
    update_pi_coin_price(exchanges)
    time.sleep(60)  # Update every minute
