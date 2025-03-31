import sqlite3
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import time
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load configuration from environment variables
DB_PATH = os.environ.get('PI_COIN_DB_PATH', 'pi_coin_value.db')
EMAIL_SERVER = os.environ.get('PI_COIN_EMAIL_SERVER', 'smtp.example.com')
EMAIL_PORT = int(os.environ.get('PI_COIN_EMAIL_PORT', 587))
EMAIL_USERNAME = os.environ.get('PI_COIN_EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.environ.get('PI_COIN_EMAIL_PASSWORD', '')
TARGET_VALUE = float(os.environ.get('PI_COIN_TARGET_VALUE', 314159.00))
EMAIL_RECIPIENT = os.environ.get('PI_COIN_EMAIL_RECIPIENT', 'you@example.com')

def init_db():
    """Initialize the database and create the necessary tables."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def store_value(value):
    """Store the current Pi coin value in the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO values (value) VALUES (?)', (value,))
            conn.commit()
            logging.info(f"Stored value: ${value:.2f}")
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def send_email(value):
    """Send an email notification about the Pi coin value."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = 'Pi Coin Value Alert'
        body = f'''
        <html>
            <body>
                <h2>Pi Coin Value Alert</h2>
                <p>The current Pi Coin value is now <strong>${value:.2f}</strong>, which is above the target value of <strong>${TARGET_VALUE:.2f}</strong>.</p>
            </body>
        </html>
        '''
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, EMAIL_RECIPIENT, msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def fetch_market_data():
    """Fetch the current market value of Pi coin from an external API."""
    try:
        response = requests.get('https://api.example.com/pi_coin_price')  # Replace with actual API
        if response.status_code == 200:
            return response.json()['price']
        else:
            logging.error("Failed to fetch market data.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def analyze_trends():
    """Analyze historical data to predict future trends."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM values ORDER BY timestamp')
            data = cursor.fetchall()
            values = np.array([row[0] for row in data]).reshape(-1, 1)
            timestamps = np.arange(len(values)).reshape(-1, 1)

            model = LinearRegression()
            model.fit(timestamps, values)
            predicted_value = model.predict(np.array([[len(values)]]))
            return predicted_value[0][0]
    except Exception as e:
        logging.error(f"Error analyzing trends: {e}")
        return None

def visualize_data():
    """Visualize historical data and predictions."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT timestamp, value FROM values ORDER BY timestamp')
            data = cursor.fetchall()
            timestamps = [row[0] for row in data]
            values = [row[1] for row in data]

            plt.figure(figsize=(10, 5))
            plt.plot(timestamps, values, label='Historical Values', marker='o')
            plt.title('Pi Coin Historical Values')
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            plt.show()
    except Exception as e:
        logging.error(f"Error visualizing data: {e}")

def main():
    """Main function to manage the Pi coin value."""
    init_db()  # Initialize the database

    while True:
        # Fetch the current market value
        current_value = fetch_market_data()
        if current_value is not None:
            store_value(current_value)

            # Check if the value has reached the target value
            if current_value >= TARGET_VALUE:
                send_email(current_value)

            # Analyze trends and visualize data
            predicted_value = analyze_trends()
            if predicted_value is not None:
                logging.info(f"Predicted next value: ${predicted_value:.2f}")
                visualize_data()

        time.sleep(60)  # Wait before checking again

if __name__ == "__main__":
    main()
