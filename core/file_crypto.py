import os, base64, secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_file(path: str, password: str) -> str:
    with open(path, "rb") as f:
        data = f.read()

    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    encrypted = Fernet(key).encrypt(data)

    filename = os.path.basename(path).encode()
    out_path = path + ".enc"

    with open(out_path, "wb") as f:
        f.write(b"FILE")
        f.write(salt)
        f.write(len(filename).to_bytes(2, "big"))
        f.write(filename)
        f.write(encrypted)

    return out_path


def decrypt_file(path: str, password: str) -> str:
    with open(path, "rb") as f:
        if f.read(4) != b"FILE":
            raise ValueError("Invalid encrypted file")

        salt = f.read(16)
        name_len = int.from_bytes(f.read(2), "big")
        original_name = f.read(name_len).decode()
        encrypted = f.read()

    key = derive_key(password, salt)
    decrypted = Fernet(key).decrypt(encrypted)

    out_path = os.path.join(os.path.dirname(path), original_name)
    with open(out_path, "wb") as f:
        f.write(decrypted)

    return out_path
