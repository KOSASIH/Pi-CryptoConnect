import socket
import logging
import os
import time

class ConnectivityTester:
    def __init__(self):
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds
        self.timeout = int(os.getenv("TIMEOUT", 5))  # seconds
        self.host = os.getenv("TEST_HOST", "8.8.8.8")  # Default to Google's public DNS

    def test_connectivity(self):
        """Test connectivity to a host."""
        try:
            with socket.create_connection((self.host, 80), timeout=self.timeout):
                logging.info(f"Successfully connected to {self.host}")
                return True
        except OSError as e:
            logging.error(f"Failed to connect to {self.host}: {e}")
            return False

    async def run(self):
        """Run the connectivity tester in an autonomous manner."""
        while True:
            self.test_connectivity()
            await asyncio.sleep(self.check_interval)
