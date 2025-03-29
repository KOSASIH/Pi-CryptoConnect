import os
import signal
import time
import logging
import asyncio
from dotenv import load_dotenv
from connectivity_tester import ConnectivityTester
from wifi_signal_monitor import WiFiSignalMonitor
from network_traffic_monitor import NetworkTrafficMonitor

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedNetworkMonitor:
    def __init__(self):
        self.connectivity_tester = ConnectivityTester()
        self.wifi_signal_monitor = WiFiSignalMonitor()
        self.network_traffic_monitor = NetworkTrafficMonitor()
        self.running = True

    async def run(self):
        """Run all monitoring tasks asynchronously."""
        while self.running:
            await asyncio.gather(
                self.connectivity_tester.run(),
                self.wifi_signal_monitor.run(),
                self.network_traffic_monitor.run()
            )

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    monitor = AdvancedNetworkMonitor()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, monitor.stop)
    signal.signal(signal.SIGTERM, monitor.stop)

    # Run the advanced network monitor
    asyncio.run(monitor.run())
