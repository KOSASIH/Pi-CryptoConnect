import requests
import time

def set_pi_coin_value(value):
    # Set the Pi coin value on global exchanges
    url = "https://api.globalexchanges.com/set_value"
    headers = {"Content-Type": "application/json"}
    data = {"value": value, "coin": "Pi", "type": "stablecoin"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Pi coin value set to:", value)
    else:
        print("Failed to set Pi coin value:", response.text)

# Set the Pi coin value to $314,159.00
set_pi_coin_value(314159.00)

# You can also set a delay between value updates
# time.sleep(60)  # Delay for 60 seconds
