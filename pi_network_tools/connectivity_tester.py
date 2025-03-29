import socket
import logging
import time
import signal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectivityTester:
    def __init__(self):
        self.running = True
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds
        self.timeout = int(os.getenv("TIMEOUT", 5))  # seconds
        self.host = os.getenv("TEST_HOST", "8.8.8.8")  # Default to Google's public DNS

    def test_connectivity(self, host):
        """
        Test connectivity to a host.
        """
        try:
            with socket.create_connection((host, 80), timeout=self.timeout):
                logging.info(f"Successfully connected to {host}")
                return True
        except OSError as e:
            logging.error(f"Failed to connect to {host}: {e}")
            return False

    def run(self):
        """Run the connectivity tester in an autonomous manner."""
        while self.running:
            self.test_connectivity(self.host)
            logging.info(f"Waiting for {self.check_interval} seconds before the next check...")
            time.sleep(self.check_interval)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    tester = ConnectivityTester()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, tester.stop)
    signal.signal(signal.SIGTERM, tester.stop)

    # Run the connectivity tester
    tester.run()
