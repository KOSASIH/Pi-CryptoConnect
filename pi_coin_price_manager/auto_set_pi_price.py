import requests

def set_pi_coin_price(price):
    # Set the Pi coin price on global exchanges
    url = "https://api.globalexchanges.com/set_price"
    headers = {"Content-Type": "application/json"}
    data = {"coin": "PI", "price": price}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Pi coin price successfully set to $314.159")
    else:
        print("Failed to set Pi coin price")

# Set the Pi coin price to $314.159
set_pi_coin_price(314.159)
