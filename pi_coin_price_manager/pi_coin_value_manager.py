import sqlite3
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load configuration from environment variables
DB_PATH = os.environ.get('PI_COIN_DB_PATH', 'pi_coin_value.db')
EMAIL_SERVER = os.environ.get('PI_COIN_EMAIL_SERVER', 'smtp.example.com')
EMAIL_PORT = int(os.environ.get('PI_COIN_EMAIL_PORT', 587))
EMAIL_USERNAME = os.environ.get('PI_COIN_EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.environ.get('PI_COIN_EMAIL_PASSWORD', '')
TARGET_VALUE = float(os.environ.get('PI_COIN_TARGET_VALUE', 314159.00))  # Set target value to $314,159.00
EMAIL_RECIPIENT = os.environ.get('PI_COIN_EMAIL_RECIPIENT', 'you@example.com')

def store_value(value):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS values (value REAL)''')
            cursor.execute('INSERT INTO values (value) VALUES (?)', (value,))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def send_email(value):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = 'Pi Coin value alert'
        body = f'The current Pi Coin value is now ${value:.2f}, which is above the target value of ${TARGET_VALUE:.2f}.'
        msg.attach(MIMEText(body))

        with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, EMAIL_RECIPIENT, msg.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

def main():
    # Set the stable value of Pi Coin
    stable_value = 314159.00
    store_value(stable_value)
    
    # Check if the value has reached the target value
    if stable_value >= TARGET_VALUE:
        send_email(stable_value)

if __name__ == "__main__":
    main()
