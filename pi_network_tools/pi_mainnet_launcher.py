import requests

def open_mainnet():
    # Set the Pi Network API endpoint
    url = "https://api.pi-network.com/open-mainnet"

    # Set the API key (if required)
    headers = {"Authorization": "Bearer <your_api_key>"}

    # Send the request to open the mainnet
    response = requests.post(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        print("Mainnet opened successfully")
    else:
        print("Failed to open mainnet:", response.text)

# Call the open_mainnet function
open_mainnet()
