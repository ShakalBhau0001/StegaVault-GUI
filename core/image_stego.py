import struct, secrets, base64
from PIL import Image
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


MAGIC = b"STEG"


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


def parse_payload(raw: bytes):
    if raw[:4] != MAGIC:
        raise ValueError("No hidden data found")

    salt = raw[4:20]
    size = struct.unpack(">I", raw[20:24])[0]
    return salt, raw[24: 24 + size]


# EMBED


def embed_message(image_path: str, message: bytes, password: str, out_path: str):
    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())

    salt = secrets.token_bytes(16)
    key = derive_key(password, salt)
    encrypted = Fernet(key).encrypt(message)
    payload = make_payload(encrypted, salt)

    bits = list(bytes_to_bits(payload))
    capacity = len(pixels) * 3

    if len(bits) > capacity:
        raise ValueError("Message too large for this image")

    new_pixels = []
    bit_i = 0

    for r, g, b, a in pixels:
        if bit_i < len(bits):
            r = (r & ~1) | bits[bit_i]
            bit_i += 1
        if bit_i < len(bits):
            g = (g & ~1) | bits[bit_i]
            bit_i += 1
        if bit_i < len(bits):
            b = (b & ~1) | bits[bit_i]
            bit_i += 1
        new_pixels.append((r, g, b, a))

    out = Image.new("RGBA", img.size)
    out.putdata(new_pixels)
    out.save(out_path, "PNG")


# EXTRACT


def extract_message(image_path: str, password: str) -> bytes:
    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())

    bits = []
    for r, g, b, _ in pixels:
        bits.extend([r & 1, g & 1, b & 1])

    header = bits_to_bytes(bits[:192])  # first 24 bytes
    if header[:4] != MAGIC:
        raise ValueError("No hidden message found")

    salt = header[4:20]
    size = struct.unpack(">I", header[20:24])[0]

    payload_bits = bits[: (24 + size) * 8]
    payload = bits_to_bytes(payload_bits)

    salt2, encrypted = parse_payload(payload)
    if salt != salt2:
        raise ValueError("Corrupted data")

    key = derive_key(password, salt)
    return Fernet(key).decrypt(encrypted)
