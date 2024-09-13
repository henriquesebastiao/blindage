import base64
import hashlib

import bcrypt
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


def hash_main_password(main_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(main_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_main_password(stored_hash: str, main_password: str) -> bool:
    return bcrypt.checkpw(
        main_password.encode('utf-8'), stored_hash.encode('utf-8')
    )
