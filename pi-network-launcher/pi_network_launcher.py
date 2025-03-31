# Pi Network Auto Global Open Mainnet Launcher

# Import necessary libraries
import os
import time
import requests
import json
import logging
import smtplib
from datetime import datetime
from requests.exceptions import RequestException
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='pi_network_launcher.log')

# Set API endpoint and API key
API_ENDPOINT = os.getenv("PI_API_ENDPOINT", "https://api.minepi.com")
API_KEY = os.getenv("PI_API_KEY", "YOUR_API_KEY_HERE")

# Set mainnet launch parameters
MAINNET_LAUNCH_DATE = "2025-03-31T00:00:00Z"  # Updated launch date
MAINNET_LAUNCH_BLOCK_HEIGHT = 100000  # Example block height

# Email configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@example.com")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver_email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")

# Function to send email notifications
def send_email_notification(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            logging.info("Email notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")

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
    send_email_notification("Mainnet Launch Notification", "The mainnet has been successfully launched.")

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

# Function to check API health
def check_api_health():
    try:
        response = requests.get(f"{API_ENDPOINT}/health", headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        logging.info("API is healthy.")
    except RequestException as e:
        logging.error(f"API health check failed: {e}")
        send_email_notification("API Health Alert", f"API health check failed: {e}")

# Main program
def main():
    check_api_health()  # Check API health before proceeding
    wait_until_launch_date()  # Wait until the launch date
    while True:
        if not is_mainnet_launched():
            launch_mainnet()
            break  # Exit the loop after launching
        else:
            logging.info("Mainnet already launched.")
            break  # Exit the loop if mainnet is already launched

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
