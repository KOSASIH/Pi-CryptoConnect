from cryptography.hazmat.primitives import hmac, serialization
from cryptography.hazmat.primitives.asymmetric import ntru, padding, utils
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# Generate a new NTRU key pair
private_key = ntru.NTRUPrivateKey.generate(ntru.SECURITY_LEVEL_128)
public_key = private_key.public_key()

# Serialize the public key
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)

# Deserialize the public key
public_key = ntru.NTRUPublicKey.from_public_bytes(
    encoding=serialization.Encoding.PEM, data=pem
)

# Encrypt data using NTRU key encapsulation
encapsulated_key, encrypted_data = public_key.encapsulate(
    utils.Message(b"This is the data to be encrypted"),
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# Decrypt data using NTRU key decapsulation
decrypted_data = private_key.decapsulate(
    encapsulated_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

# Compare the decrypted data with the original data
if decrypted_data == b"This is the data to be encrypted":
    print("Data decrypted successfully")
else:
    print("Data decryption failed")
