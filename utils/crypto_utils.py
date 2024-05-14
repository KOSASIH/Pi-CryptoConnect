# utils/crypto_utils.py

import hashlib
import hmac
import base64

def sha256(message: str) -> str:
    """Calculate the SHA-256 hash of a message"""
    return hashlib.sha256(message.encode()).hexdigest()

def hmac_sha256(key: str, message: str) -> str:
    """Calculate the HMAC-SHA-256 hash of a message"""
    return hmac.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()

def base64_encode(data: bytes) -> str:
    """Encode data in base64"""
    return base64.b64encode(data).decode()

def base64_decode(data: str) -> bytes:
    """Decode data from base64"""
    return base64.b64decode(data.encode())

def generate_private_key() -> str:
    """Generate a new private key"""
    return base64.b64encode(os.urandom(32)).decode()

def generate_public_key(private_key: str) -> str:
    """Generate a new public key from a private key"""
    private_key_bytes = base64.b64decode(private_key.encode())
    public_key_bytes = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.NIST256p).verifying_key.to_string()
    return base64.b64encode(public_key_bytes).decode()

def sign_message(private_key: str, message: str) -> str:
    """Sign a message with a private key"""
    private_key_bytes = base64.b64decode(private_key.encode())
    signer = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.NIST256p)
    signature = signer.sign(message.encode())
    return base64.b64encode(signature).decode()

def verify_signature(public_key: str, message: str, signature: str) -> bool:
    """Verify a signature with a public key"""
    public_key_bytes = base64.b64decode(public_key.encode())
    verifier = ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.NIST256p)
    signature_bytes = base64.b64decode(signature.encode())
    try:
        verifier.verify(signature_bytes, message.encode())
        return True
    except ecdsa.BadSignatureError:
        return False
