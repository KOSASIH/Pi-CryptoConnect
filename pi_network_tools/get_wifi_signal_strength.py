import subprocess


def get_wifi_signal_strength():
    """
    Get the Wi-Fi signal strength of the Raspberry Pi.
    """
    try:
        output = subprocess.check_output(["iwconfig", "wlan0"])
        match = re.search(r'ESSID:"(.*)"  \((.*)\)', output.decode())
        if match:
            signal_strength = match.group(2)
            return signal_strength
    except Exception as e:
        print(f"Error getting Wi-Fi signal strength: {e}")
    return "Unknown"
