import requests


def get_pi_coin_price():
    # Set the CoinGecko API endpoint
    url = (
        "https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd"
    )

    # Send the request to get the Pi coin price
    response = requests.get(url)

    # Check the response status code
    if response.status_code == 200:
        # Get the Pi coin price
        pi_coin_price = response.json()["pi-network"]["usd"]

        # Set the global exchanges API endpoint
        url = "https://api.global-exchanges.com/set-price"

        # Set the API key (if required)
        headers = {"Authorization": "Bearer <your_api_key>"}

        # Set the request data
        data = {"price": pi_coin_price, "coin": "Pi"}

        # Send the request to set the Pi coin price
        response = requests.post(url, headers=headers, json=data)

        # Check the response status code
        if response.status_code == 200:
            print("Pi coin price set to:", pi_coin_price)
        else:
            print("Failed to set Pi coin price:", response.text)
    else:
        print("Failed to get Pi coin price:", response.text)


# Call the get_pi_coin_price function
get_pi_coin_price()
