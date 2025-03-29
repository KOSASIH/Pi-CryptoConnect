import psutil
import logging
import os
import time

class NetworkTrafficMonitor:
    def __init__(self):
        self.check_interval = int(os.getenv("TRAFFIC_CHECK_INTERVAL", 10))  # seconds

    def get_network_traffic(self):
        """Get the network traffic of the Raspberry Pi."""
        traffic = psutil.net_io_counters(pernic=True)  # Get traffic per network interface
        traffic_info = {}
        for interface, stats in traffic.items():
            traffic_info[interface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv
            }
        return traffic_info

    async def run(self):
        """Run the network traffic monitor in an autonomous manner."""
        while True:
            traffic_info = self.get_network_traffic()
            for interface, stats in traffic_info.items():
                logging.info(f"Interface: {interface}, Bytes Sent: {stats['bytes_sent']}, Bytes Received: {stats['bytes_recv']}")
            await asyncio.sleep(self.check_interval)
