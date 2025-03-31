# Pi Network Auto Global Open Mainnet Launcher

# Import necessary libraries
import os
import time
import requests
import json
import logging
from datetime import datetime
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set API endpoint and API key
API_ENDPOINT = os.getenv("PI_API_ENDPOINT", "https://api.pi.network/v1")
API_KEY = os.getenv("PI_API_KEY", "YOUR_API_KEY_HERE")

# Set mainnet launch parameters
MAINNET_LAUNCH_DATE = "2025-03-31T00:00:00Z"  # Updated launch date
MAINNET_LAUNCH_BLOCK_HEIGHT = 100000  # Example block height

# Function to get current block height
def get_current_block_height():
    try:
        response = requests.get(f"{API_ENDPOINT}/blocks/latest", headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get("height")
    except RequestException as e:
        logging.error(f"Error fetching current block height: {e}")
        return None

# Function to check if mainnet is launched
def is_mainnet_launched():
    current_block_height = get_current_block_height()
    if current_block_height is not None:
        if current_block_height >= MAINNET_LAUNCH_BLOCK_HEIGHT:
            logging.info("Mainnet has been launched.")
            return True
        else:
            logging.info("Mainnet has not been launched yet.")
            return False
    return False

# Function to launch mainnet
def launch_mainnet():
    logging.info("Launching mainnet...")
    # Perform necessary actions to launch mainnet
    # This is a placeholder for actual launch logic
    logging.info("Mainnet launched successfully!")

# Function to wait until the mainnet launch date
def wait_until_launch_date():
    while True:
        current_time = datetime.now().isoformat() + "Z"
        if current_time >= MAINNET_LAUNCH_DATE:
            logging.info("Reached the mainnet launch date.")
            break
        else:
            logging.info("Waiting for mainnet launch date...")
            time.sleep(60)  # Check every 1 minute

# Main program
def main():
    wait_until_launch_date()  # Wait until the launch date
    while True:
        if not is_mainnet_launched():
            launch_mainnet()
            break  # Exit the loop after launching
        else:
            logging.info("Mainnet already launched.")
            break  # Exit the loop if mainnet is already launched

if __name__ == "__main__":
    main()
