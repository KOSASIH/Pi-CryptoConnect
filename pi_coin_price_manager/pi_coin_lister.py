import requests
import time

def set_pi_coin_price(price):
    # Set the Pi coin price on global exchanges
    url = "https://api.globalexchanges.com/set_price"
    headers = {"Content-Type": "application/json"}
    data = {"price": price, "coin": "Pi"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Pi coin price set to:", price)
    else:
        print("Failed to set Pi coin price:", response.text)

# Set the Pi coin price to $314.159
set_pi_coin_price(314.159)

# You can also set a delay between price updates
# time.sleep(60)  # Delay for 60 seconds
