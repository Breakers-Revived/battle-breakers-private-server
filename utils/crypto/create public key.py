"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

Utility script to generate a public key from a private key for the Battle Breakers Private Server.
"""
from os import getcwd, path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
PRIVATE_KEY_PEM_PATH = path.join(__location__, "bb_private_key.pem")
PUBLIC_KEY_PEM_PATH = path.join(__location__, "bb_public_key.pem")

# Safety check
if not path.isfile(PRIVATE_KEY_PEM_PATH):
    print("Error: We can't generate the public key without the private key.")
    print(f"Make sure \"{PRIVATE_KEY_PEM_PATH}\" exists.")
    exit(1)


# Load the private key from file
with open(PRIVATE_KEY_PEM_PATH, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=b'pw',  # Replace with your password if applicable
        backend=default_backend()
    )

# Get the public key from the private key
public_key = private_key.public_key()

# Serialize the public key to a PEM-encoded string
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the public key to a file
with open(PUBLIC_KEY_PEM_PATH, "wb") as key_file:
    key_file.write(public_pem)
