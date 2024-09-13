import base64
import hashlib

from cryptography.fernet import Fernet


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
