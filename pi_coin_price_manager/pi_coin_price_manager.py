import os
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

# Load configuration from environment variables
API_ENDPOINT = os.environ.get("PI_COIN_API_ENDPOINT", "https://api.example.com/price")
DB_PATH = os.environ.get("PI_COIN_DB_PATH", "pi_coin_price.db")
EMAIL_SERVER = os.environ.get("PI_COIN_EMAIL_SERVER", "smtp.example.com")
EMAIL_PORT = int(os.environ.get("PI_COIN_EMAIL_PORT", 587))
EMAIL_USERNAME = os.environ.get("PI_COIN_EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.environ.get("PI_COIN_EMAIL_PASSWORD", "")
TARGET_PRICE = float(os.environ.get("PI_COIN_TARGET_PRICE", 0))

# Fetch the current Pi coin price from the API
response = requests.get(API_ENDPOINT)
price = response.json()["price"]

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the prices table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS prices (price REAL)""")

# Insert the current price into the database
cursor.execute("INSERT INTO prices (price) VALUES (?)", (price,))
conn.commit()

# Check if the price has reached the target price
if price >= TARGET_PRICE:
    # Send an email notification
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = "you@example.com"
    msg["Subject"] = "Pi coin price alert"
    body = f"The current Pi coin price is now ${price:.2f}, which is above the target price of ${TARGET_PRICE:.2f}."
    msg.attach(MIMEText(body))

    # Send the email
    with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, "you@example.com", msg.as_string())

# Close the database connection
conn.close()
