import pyotp
from flask_login import UserMixin
from pi_cryptoconnect.database import db

class TwoFactorAuth:
    def __init__(self, user: UserMixin):
        self.user = user
        self.secret_key = pyotp.random_base32()

    def generate_qr_code(self) -> str:
        """
        Generate a QR code for the user to scan.

        :return: QR code URL
        """
        return pyotp.totp.TOTP(self.secret_key).provisioning_uri(self.user.username, issuer_name="Pi Crypto Connect")

    def verify_token(self, token: str) -> bool:
        """
        Verify the user's 2FA token.

        :param token: User's 2FA token
        :return: True if token is valid, False otherwise
        """
        return pyotp.totp.TOTP(self.secret_key).verify(token)

    def enable_two_factor_auth(self) -> None:
        """
        Enable two-factor authentication for the user.

        :return: None
        """
        self.user.two_factor_auth_enabled = True
        self.user.two_factor_auth_secret_key = self.secret_key
        db.session.commit()

    def disable_two_factor_auth(self) -> None:
        """
        Disable two-factor authentication for the user.

        :return: None
        """
        self.user.two_factor_auth_enabled = False
        self.user.two_factor_auth_secret_key = None
        db.session.commit()

    def get_two_factor_auth_status(self) -> bool:
        """
        Get the two-factor authentication status for the user.

        :return: True if 2FA is enabled, False otherwise
        """
        return self.user.two_factor_auth_enabled

    def get_two_factor_auth_secret_key(self) -> str:
        """
        Get the two-factor authentication secret key for the user.

        :return: Secret key
        """
        return self.user.two_factor_auth_secret_key
