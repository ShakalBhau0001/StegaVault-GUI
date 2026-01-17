import wave
import struct
import secrets
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


MAGIC = b"AUDS"


# KEY


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


# BIT HELPERS


def bytes_to_bits(data: bytes):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1


def bits_to_bytes(bits):
    out = bytearray()
    for i in range(0, len(bits), 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        out.append(b)
    return bytes(out)


# PAYLOAD


def make_payload(encrypted: bytes, salt: bytes) -> bytes:
    return MAGIC + salt + struct.pack(">I", len(encrypted)) + encrypted


def parse_payload(data: bytes):
    if data[:4] != MAGIC:
        raise ValueError("No hidden audio data found")

    salt = data[4:20]
    size = struct.unpack(">I", data[20:24])[0]
    return salt, data[24 : 24 + size]


# EMBED


def embed_audio(wav_path: str, message: bytes, password: str, out_path: str):
    with wave.open(wav_path, "rb") as w:
        params = w.getparams()
        frames = bytearray(w.readframes(w.getnframes()))

    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    encrypted = Fernet(key).encrypt(message)
    payload = make_payload(encrypted, salt)

    bits = list(bytes_to_bits(payload))
    capacity = len(frames)

    if len(bits) > capacity:
        raise ValueError("Message too large for this audio file")

    for i, bit in enumerate(bits):
        frames[i] = (frames[i] & 0b11111110) | bit

    with wave.open(out_path, "wb") as w:
        w.setparams(params)
        w.writeframes(frames)


# EXTRACT


def extract_audio(wav_path: str, password: str) -> bytes:
    with wave.open(wav_path, "rb") as w:
        frames = bytearray(w.readframes(w.getnframes()))

    bits = [b & 1 for b in frames]

    header = bits_to_bytes(bits[:192])  # 24 bytes
    if header[:4] != MAGIC:
        raise ValueError("No hidden message found")

    salt = header[4:20]
    size = struct.unpack(">I", header[20:24])[0]

    payload_bits = bits[: (24 + size) * 8]
    payload = bits_to_bytes(payload_bits)

    salt2, encrypted = parse_payload(payload)
    if salt != salt2:
        raise ValueError("Corrupted audio data")

    key = derive_key(password, salt)
    return Fernet(key).decrypt(encrypted)
