import subprocess
import re
import logging
import os
import time

class WiFiSignalMonitor:
    def __init__(self):
        self.check_interval = int(os.getenv("CHECK_INTERVAL", 10))  # seconds
        self.interface = os.getenv("WIFI_INTERFACE", "wlan0")  # Default to wlan0

    def get_wifi_signal_strength(self):
        """Get the Wi-Fi signal strength of the Raspberry Pi."""
        try:
            output = subprocess.check_output(['iwconfig', self.interface])
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

    async def run(self):
        """Run the Wi-Fi signal monitor in an autonomous manner."""
        while True:
            ssid, signal_strength = self.get_wifi_signal_strength()
            logging.info(f"SSID: {ssid}, Signal Strength: {signal_strength}")
            await asyncio.sleep(self.check_interval)
