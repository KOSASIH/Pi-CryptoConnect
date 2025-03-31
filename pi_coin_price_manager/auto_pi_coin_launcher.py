import os
import time
import ccxt
import logging
import smtplib
from email.mime.text import MIMEText
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename='trading_bot.log',
                    filemode='a')  # Append mode

# Load configuration from environment variables
API_KEY = os.getenv("BINANCE_API_KEY", "YOUR_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "YOUR_SECRET_KEY")
TARGET_VALUE = float(os.getenv("TARGET_VALUE", 314159.00))  # Set as a stablecoin value
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@example.com")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")

# Initialize exchanges
exchanges = {
    'binance': ccxt.binance({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
    }),
    'kucoin': ccxt.kucoin({
        'apiKey': os.getenv("KUCOIN_API_KEY", "YOUR_KUCOIN_API_KEY"),
        'secret': os.getenv("KUCOIN_SECRET_KEY", "YOUR_KUCOIN_SECRET_KEY"),
        'password': os.getenv("KUCOIN_PASSWORD", "YOUR_KUCOIN_PASSWORD"),
    }),
    'bitfinex': ccxt.bitfinex({
        'apiKey': os.getenv("BITFINEX_API_KEY", "YOUR_BITFINEX_API_KEY"),
        'secret': os.getenv("BITFINEX_SECRET_KEY", "YOUR_BITFINEX_SECRET_KEY"),
    }),
    'okx': ccxt.okx({
        'apiKey': os.getenv("OKX_API_KEY", "YOUR_OKX_API_KEY"),
        'secret': os.getenv("OKX_SECRET_KEY", "YOUR_OKX_SECRET_KEY"),
        'password': os.getenv("OKX_PASSWORD", "YOUR_OKX_PASSWORD"),
    }),
    'bitget': ccxt.bitget({
        'apiKey': os.getenv("BITGET_API_KEY", "YOUR_BITGET_API_KEY"),
        'secret': os.getenv("BITGET_SECRET_KEY", "YOUR_BITGET_SECRET_KEY"),
        'password': os.getenv("BITGET_PASSWORD", "YOUR_BITGET_PASSWORD"),
    }),
    'bittrex': ccxt.bittrex({
        'apiKey': os.getenv("BITTREX_API_KEY", "YOUR_BITTREX_API_KEY"),
        'secret': os.getenv("BITTREX_SECRET_KEY", "YOUR_BITTREX_SECRET_KEY"),
    }),
    'kraken': ccxt.kraken({
        'apiKey': os.getenv("KRAKEN_API_KEY", "YOUR_KRAKEN_API_KEY"),
        'secret': os.getenv("KRAKEN_SECRET_KEY", "YOUR_KRAKEN_SECRET_KEY"),
    }),
    'indodax': ccxt.indodax({
        'apiKey': os.getenv("INDODAX_API_KEY", "YOUR_INDODAX_API_KEY"),
        'secret': os.getenv("INDODAX_SECRET_KEY", "YOUR_INDODAX_SECRET_KEY"),
    }),
    'gateio': ccxt.gateio({
        'apiKey': os.getenv("GATEIO_API_KEY", "YOUR_GATEIO_API_KEY"),
        'secret': os.getenv("GATEIO_SECRET_KEY", "YOUR_GATEIO_SECRET_KEY"),
    }),
    'huobipro': ccxt.huobipro({
        'apiKey': os.getenv("HUOBI_API_KEY", "YOUR_HUOBI_API_KEY"),
        'secret': os.getenv("HUOBI_SECRET_KEY", "YOUR_HUOBI_SECRET_KEY"),
    }),
    'phemex': ccxt.phemex({
        'apiKey': os.getenv("PHEMEX_API_KEY", "YOUR_PHEMEX_API_KEY"),
        'secret': os.getenv("PHEMEX_SECRET_KEY", "YOUR_PHEMEX_SECRET_KEY"),
    }),
    # Add more exchanges as needed
}

# Function to send email notifications
def send_email_notification(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            logging.info("Email notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")

# Function to monitor a single exchange
def monitor_exchange(exchange_name, exchange):
    while True:
        try:
            # Check the health of the exchange
            exchange.load_markets()
            ticker = exchange.fetch_ticker('PI/USDT')

            # Check if the last value is greater than or equal to the target value
            if ticker['last'] >= TARGET_VALUE:
                # Send an alert
                message = f'{exchange_name.capitalize()} - PI Coin has reached the target value of ${TARGET_VALUE:.2f}!'
                print(message)
                logging.info(message)
                send_email_notification("Target Value Reached", message)

        except ccxt.NetworkError as e:
            logging.error(f'Network error on {exchange_name}: {e}')
            time.sleep(10)  # Wait before retrying
        except ccxt.ExchangeError as e:
            logging.error(f'Exchange error on {exchange_name}: {e}')
            time.sleep(10)  # Wait before retrying
        except Exception as e:
            logging.error(f'An unexpected error occurred on {exchange_name}: {e}')
            time.sleep(10)  # Wait before retrying

        # Wait for a short period before checking again
        time.sleep(10)

# Start monitoring each exchange in a separate thread
threads = []
for exchange_name, exchange in exchanges.items():
    thread = Thread(target=monitor_exchange, args=(exchange_name, exchange))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete (they won't, since they run indefinitely)
for thread in threads:
    thread.join()
