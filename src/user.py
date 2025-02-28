# src/user.py

import random
import re

class User:
    def __init__(self, username, phone_number):
        self.username = username
        self.phone_number = phone_number

    def __str__(self):
        return f"User: {self.username}, Phone: {self.phone_number}"

    def update_phone_number(self, new_phone_number):
        """Update the user's phone number after verification."""
        if not is_valid_phone_number(new_phone_number):
            return "Invalid phone number format. Please enter a 10-digit number."

        verification_code = send_verification_code(new_phone_number)
        user_input_code = input("Enter the verification code sent to your new phone number: ")

        if user_input_code != verification_code:
            return "Verification failed. Phone number not changed."

        self.phone_number = new_phone_number
        return "Phone number updated successfully."

def is_valid_phone_number(phone_number):
    """Check if the phone number is valid (10 digits)."""
    return re.match(r'^\d{10}$', phone_number) is not None

def send_verification_code(phone_number):
    """Simulate sending a verification code to the user's phone number."""
    verification_code = str(random.randint(100000, 999999))
    print(f"Verification code sent to {phone_number}: {verification_code}")
    return verification_code

def change_phone_number(user):
    """Prompt the user to change their phone number."""
    new_phone = input("Enter your new phone number (10 digits): ")
    result = user.update_phone_number(new_phone)
    print(result)

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Sample user for demonstration
    user = User("john_doe", "1234567890")
    print(user)  # Display current user info
    change_phone_number(user)  # Allow user to change phone number
    print(user)  # Display updated user info
