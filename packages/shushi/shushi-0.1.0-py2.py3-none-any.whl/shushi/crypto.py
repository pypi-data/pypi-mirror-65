import base64
import json
import os

from .exceptions import IncorrectPassword

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt(salt: bytes, password: str, dec_data: dict) -> bytes:
    fernet = make_fernet(salt, password)
    datastr = json.dumps(dec_data)
    return fernet.encrypt(datastr.encode())


def decrypt(salt: bytes, password: str, enc_data: bytes) -> dict:
    fernet = make_fernet(salt, password)
    try:
        raw = fernet.decrypt(enc_data)
    except InvalidToken:
        raise IncorrectPassword("Supplied password was incorrect.")
    raw_str = raw.decode()
    return json.loads(raw_str)


def make_fernet(salt: bytes, password: str) -> Fernet:
    kdf = _kdf(salt)
    key = _key(kdf, password.encode())
    return _fernet(key)


# TODO: Method not needed in this module.
def _salt():
    return os.urandom(16)


def _kdf(salt):
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )


def _key(kdf, password):
    return base64.urlsafe_b64encode(kdf.derive(password))


def _fernet(key):
    return Fernet(key)
