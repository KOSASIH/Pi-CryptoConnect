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

class IPAddressManager:
    def __init__(self):
        self.running = True
        self.previous_ip = None
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds

    def get_ip_address(self):
        """
        Get the IP address of the Raspberry Pi.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            logging.error(f"Error retrieving IP address: {e}")
            return None

    def notify_ip_change(self, new_ip):
        """
        Notify the user of an IP address change.
        """
        logging.info(f"IP address changed to: {new_ip}")
        # Here you can implement additional notification logic (e.g., email, SMS)

    def run(self):
        """Run the IP address manager in an autonomous manner."""
        while self.running:
            current_ip = self.get_ip_address()
            if current_ip:
                if current_ip != self.previous_ip:
                    self.notify_ip_change(current_ip)
                    self.previous_ip = current_ip
            time.sleep(self.check_interval)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    manager = IPAddressManager()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, manager.stop)
    signal.signal(signal.SIGTERM, manager.stop)

    # Run the IP address manager
    manager.run()
