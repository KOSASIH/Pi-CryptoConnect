# src/user.py

import json
import random
import re
import hashlib
import os

class User:
    def __init__(self, username, phone_number, password):
        self.username = username
        self.phone_number = phone_number
        self.password_hash = self.hash_password(password)
        self.portfolio = {}  # Dictionary to hold currency and amount
        self.transactions = []  # List to hold transaction history

    def __str__(self):
        return f"User: {self.username}, Phone: {self.phone_number}, Portfolio: {self.portfolio}"

    @staticmethod
    def hash_password(password):
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        return self.password_hash == self.hash_password(password)

    def update_phone_number(self, new_phone_number):
        if not is_valid_phone_number(new_phone_number):
            return "Invalid phone number format. Please enter a 10-digit number."

        verification_code = send_verification_code(new_phone_number)
        user_input_code = input("Enter the verification code sent to your new phone number: ")

        if user_input_code != verification_code:
            return "Verification failed. Phone number not changed."

        self.phone_number = new_phone_number
        return "Phone number updated successfully."

    def add_currency(self, currency, amount):
        """Add a currency to the user's portfolio."""
        if currency in self.portfolio:
            self.portfolio[currency] += amount
        else:
            self.portfolio[currency] = amount
        self.transactions.append(Transaction(currency, amount, 'buy'))

    def remove_currency(self, currency, amount):
        """Remove a currency from the user's portfolio."""
        if currency in self.portfolio and self.portfolio[currency] >= amount:
            self.portfolio[currency] -= amount
            if self.portfolio[currency] == 0:
                del self.portfolio[currency]
            self.transactions.append(Transaction(currency, amount, 'sell'))
            return f"Removed {amount} of {currency} from portfolio."
        return "Insufficient amount or currency not found."

    def save_user_data(self):
        """Save user data to a JSON file."""
        user_data = {
            'username': self.username,
            'phone_number': self.phone_number,
            'password_hash': self.password_hash,
            'portfolio': self.portfolio,
            'transactions': [str(tx) for tx in self.transactions]
        }
        with open(f"{self.username}.json", 'w') as f:
            json.dump(user_data, f)

    @staticmethod
    def load_user_data(username):
        """Load user data from a JSON file."""
        if os.path.exists(f"{username}.json"):
            with open(f"{username}.json", 'r') as f:
                data = json.load(f)
                user = User(data['username'], data['phone_number'], data['password_hash'])
                user.portfolio = data['portfolio']
                user.transactions = data['transactions']
                return user
        return None

class Transaction:
    def __init__(self, currency, amount, transaction_type):
        self.currency = currency
        self.amount = amount
        self.transaction_type = transaction_type  # 'buy' or 'sell'

    def __str__(self):
        return f"{self.transaction_type.capitalize()} {self.amount} of {self.currency}"

def is_valid_phone_number(phone_number):
    return re.match(r'^\d{10}$', phone_number) is not None

def send_verification_code(phone_number):
    verification_code = str(random.randint(100000, 999999))
    print(f"Verification code sent to {phone_number}: {verification_code}")
    return verification_code

def register_user(username, phone_number, password):
    """Register a new user."""
    if User.load_user_data(username):
        return "Username already exists. Please choose a different username."
    user = User(username, phone_number, password)
    user.save_user_data()
    return "User registered successfully."

def login_user(username, password):
    """Login an existing user."""
    user = User.load_user_data(username)
    if user and user.verify_password (password):
        return user
    return "Invalid username or password."

def main():
    action = input("Do you want to (1) Register or (2) Login? ")
    if action == '1':
        username = input("Enter your username: ")
        phone_number = input("Enter your phone number (10 digits): ")
        password = input("Enter your password: ")
        print(register_user(username, phone_number, password))
    elif action == '2':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login_user(username, password)
        if isinstance(user, User):
            print(f"Welcome back, {user.username}!")
            # Proceed to main application logic
        else:
            print(user)
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
