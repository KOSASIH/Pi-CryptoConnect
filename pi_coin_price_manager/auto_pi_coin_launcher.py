import ccxt
import time

# Initialize the exchange with your API credentials
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

# Define the trading pair and target value
trading_pair = 'PI/USDT'
target_value = 314159.00  # Set as a stablecoin value

# Loop indefinitely
while True:
    try:
        # Retrieve the ticker data for the trading pair
        ticker = exchange.fetch_ticker(trading_pair)

        # Check if the last value is greater than or equal to the target value
        if ticker['last'] >= target_value:
            # Send an alert
            print(f'PI Coin has reached the target value of ${target_value:.2f}!')

            # Optionally, you can break the loop or take further action here
            # break  # Uncomment this line if you want to stop after the alert

        # Wait for 10 seconds before checking again
        time.sleep(10)

    except ccxt.NetworkError as e:
        print(f'Network error: {e}')
        time.sleep(10)  # Wait before retrying
    except ccxt.ExchangeError as e:
        print(f'Exchange error: {e}')
        time.sleep(10)  # Wait before retrying
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        time.sleep(10)  # Wait before retrying
