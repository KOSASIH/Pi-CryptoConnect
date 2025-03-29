import os
import requests
import logging
import time
import signal
import asyncio
from dotenv import load_dotenv
from retrying import retry

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PiCoinManager:
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd"
        self.global_exchanges_url = "https://api.global-exchanges.com/set-price"
        self.api_key = os.getenv("API_KEY")
        self.stable_value = 314159.00  # Fallback stable value for Pi Coin
        self.retry_attempts = int(os.getenv("RETRY_ATTEMPTS", 3))
        self.retry_delay = int(os.getenv("RETRY_DELAY", 5))  # seconds
        self.running = True

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    async def get_pi_coin_price(self):
        """Get the current price of Pi Coin from CoinGecko."""
        try:
            response = requests.get(self.coingecko_url)
            response.raise_for_status()  # Raise an error for bad responses
            pi_coin_price = response.json()["pi-network"]["usd"]
            logging.info(f"Current Pi Coin price: ${pi_coin_price}")
            return pi_coin_price
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching Pi Coin price: {e}")
            return None

    async def set_pi_coin_price(self, price):
        """Set the Pi Coin price on the global exchanges API."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"price": price, "coin": "Pi"}

        try:
            response = requests.post(self.global_exchanges_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f"Pi Coin price set to: ${price}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to set Pi Coin price: {e}")

    async def notify_exchanges(self):
        """Notify all exchanges about the Pi Coin listing."""
        # This is a placeholder for the actual implementation
        logging.info("Notifying all exchanges about the Pi Coin listing...")

    async def run(self):
        """Run the price management system in an autonomous manner."""
        while self.running:
            price = await self.get_pi_coin_price()
            if price is None:
                logging.info(f"Using fallback stable value: ${self.stable_value}")
                price = self.stable_value
            
            await self.set_pi_coin_price(price)
            await self.notify_exchanges()  # Notify exchanges about the listing
            logging.info(f"Waiting for {self.retry_delay} seconds before the next update...")
            await asyncio.sleep(self.retry_delay)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    manager = PiCoinManager()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, manager.stop)
    signal.signal(signal.SIGTERM, manager.stop)

    # Run the Pi Coin manager
    asyncio.run(manager.run())
