import base64
import hashlib

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from cryptography.fernet import Fernet

ph = PasswordHasher()


def gen_key(main_password: str) -> bytes:
    sha256 = hashlib.sha256(main_password.encode()).digest()
    return base64.urlsafe_b64encode(sha256[:32])


def encrypt(main_password: str, text: str) -> bytes:
    key = gen_key(main_password)
    fernet = Fernet(key)
    return fernet.encrypt(text.encode())


def decrypt(main_password: str, encrypted_password: bytes) -> str:
    key = gen_key(main_password)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()


def hash_main_password(main_password: str) -> str:
    return ph.hash(main_password)


def verify_main_password(stored_hash: str, main_password: str) -> bool:
    try:
        ph.verify(stored_hash.encode('utf-8'), main_password.encode('utf-8'))
        return True
    except VerificationError:
        return False
