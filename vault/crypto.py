import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

BLOCK_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 4096

def pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS, hmac_hash_module=SHA256)

def encrypt_file(input_path: str, output_path: str, password: str):
    with open(input_path, "rb") as f:
        plaintext = pad(f.read())

    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    with open(output_path, "wb") as f:
        f.write(salt + iv + ciphertext)

def decrypt_file(input_path: str, output_path: str, password: str) -> bool:
    try:
        with open(input_path, "rb") as f:
            data = f.read()

        salt = data[:16]
        iv = data[16:32]
        ciphertext = data[32:]

        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(plaintext)

        with open(output_path, "wb") as f:
            f.write(plaintext)

        return True
    except Exception as e:
        return False
