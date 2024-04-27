import hashlib
from random import choice
from string import ascii_letters


def random_string(length: int = 12) -> str:
    return ''.join(choice(ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = random_string()
    enc = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed
