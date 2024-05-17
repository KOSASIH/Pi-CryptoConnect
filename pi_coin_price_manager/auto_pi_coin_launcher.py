import ccxt
import time

# Initialize the exchange
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

# Define the trading pair and target price
trading_pair = 'PI/USDT'
target_price = 314159

# Loop indefinitely
while True:
    # Retrieve the ticker data for the trading pair
    ticker = exchange.fetch_ticker(trading_pair)

    # Check if the last price is greater than or equal to the target price
    if ticker['last'] >= target_price:
        # Send an alert
        print(f'Pi Coin has reached the target price of ${target_price}!')

    # Wait for 10 seconds before checking again
    time.sleep(10)
