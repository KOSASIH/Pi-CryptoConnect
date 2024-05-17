import binascii
import hashlib
import random

import ecdsa

# Define the secp256k1 curve
curve = ecdsa.NIST256p()

# Alice generates her key pair
alice_private_key = ecdsa.SigningKey.generate(curve=curve)
alice_public_key = alice_private_key.get_verifying_key()

# Bob generates his key pair
bob_private_key = ecdsa.SigningKey.generate(curve=curve)
bob_public_key = bob_private_key.get_verifying_key()

# Alice generates a random number r_a and computes R_a = r_a * G
r_a = random.randint(1, curve.order - 1)
R_a = curve.generator * r_a

# Bob generates a random number r_b and computes R_b = r_b * G
r_b = random.randint(1, curve.order - 1)
R_b = curve.generator * r_b

# Alice and Bob exchange R_a and R_b

# Alice creates a transaction with the following conditions:
# - Hashlock: H(R_a || R_b || amount)
# - Timelock: t_a
# Amount: amount
alice_transaction = {
    "hashlock": hashlib.sha256(
        R_a.to_string()
        + R_b.to_string()
        + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
    ).digest(),
    "timelock": t_a,
    "amount": amount,
    "sender": alice_public_key,
    "receiver": bob_public_key,
}

# Bob creates a transaction with the following conditions:
# - Hashlock: H(R_a || R_b || amount)
# - Timelock: t_b
# Amount: amount
bob_transaction = {
    "hashlock": hashlib.sha256(
        R_a.to_string()
        + R_b.to_string()
        + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
    ).digest(),
    "timelock": t_b,
    "amount": amount,
    "sender": bob_public_key,
    "receiver": alice_public_key,
}

# Alice and Bob exchange the transactions

# Alice signs the transaction
signature = alice_private_key.sign(binascii.hexlify(alice_transaction["hashlock"]))
alice_transaction["signature"] = binascii.unhexlify(signature.encode("ascii"))

# Bob signs the transaction
signature = bob_private_key.sign(binascii.hexlify(bob_transaction["hashlock"]))
bob_transaction["signature"] = binascii.unhexlify(signature.encode("ascii"))

# Alice and Bob broadcast the transactions to their respective networks

# Once the timelock has expired, Alice and Bob reveal their secrets r_a and r_b
# They can then compute the shared secret S = r_a * r_b * G
# They can use this shared secret to unlock the funds in the other person's transaction
