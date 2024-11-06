"""
Battle Breakers Private Server / Master Control Program ""Emulator"" Copyright 2024 by Alexander Hanson (Dippyshere).
Please do not skid my hard work.
https://github.com/dippyshere/battle-breakers-private-server
This code is licensed under the Breakers Revived License (BRL).

This file contains PEM key files config
"""
from os import getcwd, path

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
PRIVATE_KEY_PEM_PATH: str = path.join(__location__, "bb_private_key.pem")
PUBLIC_KEY_PEM_PATH: str = path.join(__location__, "bb_public_key.pem")
PRIVATE_KEY_PASSWORD: bytes = b"pw"