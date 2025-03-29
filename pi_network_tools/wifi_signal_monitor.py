import subprocess
import re
import logging
import time
import signal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WiFiSignalMonitor:
    def __init__(self):
        self.running = True
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds

    def get_wifi_signal_strength(self):
        """
        Get the Wi-Fi signal strength of the Raspberry Pi.
        """
        try:
            output = subprocess.check_output(['iwconfig', 'wlan0'])
            match = re.search(r'ESSID:"(.*)"  \((.*)\)', output.decode())
            if match:
                ssid = match.group(1)
                signal_strength = match.group(2)
                return ssid, signal_strength
        except subprocess.CalledProcessError as e:
            logging.error(f'Error executing iwconfig: {e}')
        except Exception as e:
            logging.error(f'Error getting Wi-Fi signal strength: {e}')
        return 'Unknown', 'Unknown'

    def notify_signal_change(self, ssid, signal_strength):
        """
        Notify the user of the current Wi-Fi signal strength.
        """
        logging.info(f"SSID: {ssid}, Signal Strength: {signal_strength}")

    def run(self):
        """Run the Wi-Fi signal monitor in an autonomous manner."""
        while self.running:
            ssid, signal_strength = self.get_wifi_signal_strength()
            self.notify_signal_change(ssid, signal_strength)
            logging.info(f"Waiting for {self.check_interval} seconds before the next check...")
            time.sleep(self.check_interval)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    monitor = WiFiSignalMonitor()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, monitor.stop)
    signal.signal(signal.SIGTERM, monitor.stop)

    # Run the Wi-Fi signal monitor
    monitor.run()
