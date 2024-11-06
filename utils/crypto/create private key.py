"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Utility script to generate a private key for the Battle Breakers Private Server.
"""
from key_config import PRIVATE_KEY_PEM_PATH, PRIVATE_KEY_PASSWORD
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


# Generate the private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Define the encryption algorithm and encryption options
encryption_algorithm = serialization.BestAvailableEncryption(PRIVATE_KEY_PASSWORD)  # Change the password here

# Serialize the private key to PEM format with encryption
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=encryption_algorithm
)

# Save the private key to a file
with open(PRIVATE_KEY_PEM_PATH, 'wb') as f:
    f.write(private_key_pem)
