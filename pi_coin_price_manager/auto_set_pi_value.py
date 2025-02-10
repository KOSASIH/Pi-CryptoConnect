import requests

def set_pi_coin_value(value):
    # Set the Pi coin value on global exchanges
    url = "https://api.globalexchanges.com/set_value"
    headers = {"Content-Type": "application/json"}
    data = {"coin": "PI", "value": value}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Pi Coin as stable Coin with value ${value:,.2f}")
    else:
        print("Failed to set Pi coin value")

# Set the Pi coin value to $314,159.00
set_pi_coin_value(314159.00)
