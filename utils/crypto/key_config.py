from os import getcwd, path

__location__ = path.realpath(path.join(getcwd(), path.dirname(__file__)))
PRIVATE_KEY_PEM_PATH: str = path.join(__location__, "bb_private_key.pem")
PUBLIC_KEY_PEM_PATH: str = path.join(__location__, "bb_public_key.pem")
PRIVATE_KEY_PASSWORD: bytes = b"pw"