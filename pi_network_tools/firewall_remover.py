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

class PiNetworkFirewallRemover:
    def __init__(self):
        self.api_url = os.getenv("PI_NETWORK_API_URL", "https://api.minepi.com/firewall-remove")
        self.api_key = os.getenv("PI_NETWORK_API_KEY")
        self.retry_attempts = int(os.getenv("RETRY_ATTEMPTS", 3))
        self.retry_delay = int(os.getenv("RETRY_DELAY", 5))  # seconds
        self.running = True

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    async def remove_firewall(self):
        """Remove the firewall from the Pi Network."""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.post(self.api_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info("Firewall removed successfully")
            return True
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
        return False

    async def health_check(self):
        """Check the health of the API endpoint."""
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                logging.info("API is healthy.")
                return True
            else:
                logging.warning("API is not healthy.")
                return False
        except requests.RequestException as e:
            logging.error(f"Error checking API health: {e}")
            return False

    async def run(self):
        """Run the firewall remover in an autonomous manner."""
        while self.running:
            if await self.health_check():
                success = await self.remove_firewall()
                if success:
                    break
            logging.info(f"Retrying in {self.retry_delay} seconds...")
            await asyncio.sleep(self.retry_delay)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    remover = PiNetworkFirewallRemover()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, remover.stop)
    signal.signal(signal.SIGTERM, remover.stop)

    # Run the firewall remover
    asyncio.run(remover.run())
