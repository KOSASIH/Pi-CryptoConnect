import psutil
import logging
import time
import signal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkTrafficMonitor:
    def __init__(self):
        self.running = True
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds

    def get_network_traffic(self):
        """
        Get the network traffic of the Raspberry Pi.
        """
        traffic = psutil.net_io_counters(pernic=True)  # Get traffic per network interface
        traffic_info = {}
        for interface, stats in traffic.items():
            traffic_info[interface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv
            }
        return traffic_info

    def notify_traffic_change(self, traffic_info):
        """
        Notify the user of the current network traffic.
        """
        for interface, stats in traffic_info.items():
            logging.info(f"Interface: {interface}, Bytes Sent: {stats['bytes_sent']}, Bytes Received: {stats['bytes_recv']}")

    def run(self):
        """Run the network traffic monitor in an autonomous manner."""
        while self.running:
            traffic_info = self.get_network_traffic()
            self.notify_traffic_change(traffic_info)
            logging.info(f"Waiting for {self.check_interval} seconds before the next check...")
            time.sleep(self.check_interval)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    monitor = NetworkTrafficMonitor()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, monitor.stop)
    signal.signal(signal.SIGTERM, monitor.stop)

    # Run the network traffic monitor
    monitor.run()
