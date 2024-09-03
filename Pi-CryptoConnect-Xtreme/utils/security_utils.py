import hashlib
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class SecurityUtils:
    @staticmethod
    def hash_password(password):
        salt = os.urandom(16)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt, hashed_password

    @staticmethod
    def verify_password(password, salt, hashed_password):
        new_hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hmac.compare_digest(new_hashed_password, hashed_password)

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    @staticmethod
    def encrypt_data(data, key):
        cipher = Cipher(algorithms.AES(key), modes.CBC(os.urandom(16)), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_data(encrypted_data, key):
        cipher = Cipher(algorithms.AES(key), modes.CBC(encrypted_data[:16]), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(encrypted_data[16:]) + decryptor.finalize()
