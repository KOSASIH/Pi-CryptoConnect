import os
import time
import requests
import logging
import threading
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression
from email.mime.text import MIMEText
import smtplib
import json

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename='pi_coin_manager.log',
                    filemode='a')  # Append mode

# Load configuration from environment variables
TARGET_VALUE = float(os.getenv("TARGET_VALUE", 314159.00))  # Default target value
API_URL = os.getenv("API_URL", "https://api.globalexchanges.com/set_value")
DB_NAME = 'pi_coin_data.db'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS market_data (
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_market_data(price):
    """Log market data to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO market_data (price) VALUES (?)', (price,))
    conn.commit()
    conn.close()

def fetch_market_data():
    """Fetch current market data from an API."""
    # Placeholder for actual market data retrieval
    # In a real implementation, you would fetch this from an exchange or market data API
    return TARGET_VALUE  # Simulating that the market value is equal to the target value

def set_pi_coin_value(value):
    """Set the Pi coin value on global exchanges."""
    headers = {"Content-Type": "application/json"}
    data = {"coin": "Pi", "value": value, "type": "stablecoin"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            logging.info(f"Pi Coin value set to: ${value:,.2f}")
            print(f"Pi Coin value set to: ${value:,.2f}")
        else:
            logging.error(f"Failed to set Pi coin value: {response.text}")
            print("Failed to set Pi coin value:", response.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        print("Request failed:", e)

def analyze_market_conditions():
    """Analyze market conditions to detect manipulation and predict future prices."""
    while True:
        current_market_value = fetch_market_data()
        log_market_data(current_market_value)

        # Example manipulation detection logic
        if current_market_value < TARGET_VALUE * 0.95:  # Example condition for manipulation
            new_value = TARGET_VALUE * 0.95  # Adjust value to counter manipulation
            set_pi_coin_value(new_value)
        
        elif current_market_value > TARGET_VALUE * 1.05:  # Another condition for manipulation
            new_value = TARGET_VALUE * 1.05  # Adjust value to counter manipulation
            set_pi_coin_value(new_value)

        # Predict future price using a simple linear regression model
        predict_future_price()
        
        time.sleep(60)  # Wait before checking again

def predict_future_price():
    """Predict future price using historical market data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, price FROM market_data ORDER BY timestamp')
    data = cursor.fetchall()
    conn.close()

    if len(data) < 2:
        return  # Not enough data to make a prediction

    # Prepare data for linear regression
    X = np.array([row[0] for row in data]).reshape(-1, 1)  # Row IDs as features
    y = np.array([row[1] for row in data])  # Prices as target

    model = LinearRegression()
    model.fit(X, y)

    # Predict the next price
    next_row_id = len(data) + 1
    predicted_price = model.predict(np.array([[next_row_id]]))[0]
    logging.info(f"Predicted next price: ${predicted_price:,.2f}")

def send_email_notification(subject, message):
    """Send email notifications."""
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = os.getenv("EMAIL_SENDER")
        msg['To'] = os.getenv("EMAIL_RECEIVER")

        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_RECEIVER"), msg.as_string())
            logging.info("Email notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")

def monitor_health():
    """Monitor the health of the API and log status."""
    while True:
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                logging.info("API is healthy.")
            else:
                logging.warning(f"API health check failed: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"API health check failed: {e}")
        
        time.sleep(300)  # Check health every 5 minutes

if __name__ == "__main__":
    init_db()  # Initialize the database
    set_pi_coin_value(TARGET_VALUE)  # Set the initial Pi coin value
    
    # Start market analysis and health monitoring in separate threads
    market_thread = threading.Thread(target=analyze_market_conditions)
    health_thread = threading.Thread(target=monitor_health)

    market_thread.start()
    health_thread.start()

    market_thread.join()
    health_thread.join()
