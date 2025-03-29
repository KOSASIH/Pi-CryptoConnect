import netifaces
import logging
import time
import signal
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkInterfaceManager:
    def __init__(self):
        self.running = True
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds

    def get_network_interfaces(self):
        """
        Get the network interfaces of the Raspberry Pi.
        """
        interfaces = netifaces.interfaces()
        results = []
        for interface in interfaces:
            try:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    ip_address = addrs[netifaces.AF_INET][0]['addr']
                    mac_address = addrs[netifaces.AF_LINK][0]['addr']
                    status = "UP" if netifaces.ifup(interface) else "DOWN"
                    results.append({
                        "interface": interface,
                        "ip_address": ip_address,
                        "mac_address": mac_address,
                        "status": status
                    })
            except Exception as e:
                logging.error(f'Error getting network interface {interface}: {e}')
        return results

    def notify_interface_change(self, interfaces):
        """
        Notify the user of the current network interfaces.
        """
        for iface in interfaces:
            logging.info(f"Interface: {iface['interface']}, IP: {iface['ip_address']}, MAC: {iface['mac_address']}, Status: {iface['status']}")

    def run(self):
        """Run the network interface manager in an autonomous manner."""
        while self.running:
            interfaces = self.get_network_interfaces()
            self.notify_interface_change(interfaces)
            logging.info(f"Waiting for {self.check_interval} seconds before the next check...")
            time.sleep(self.check_interval)

    def stop(self, signum, frame):
        """Handle termination signals for graceful shutdown."""
        logging.info("Received shutdown signal. Stopping...")
        self.running = False

if __name__ == "__main__":
    manager = NetworkInterfaceManager()
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, manager.stop)
    signal.signal(signal.SIGTERM, manager.stop)

    # Run the network interface manager
    manager.run()
