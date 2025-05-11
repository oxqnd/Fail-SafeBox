import os
import uuid
from config import ENCRYPTED_DIR
from vault.crypto import encrypt_file
from vault.autodestruct import handle_decryption_attempt
from vault.mapper import map_filename, resolve_original_name
from vault.autodelete import delete_after_delay

def encrypt_and_map(input_path: str, password: str) -> str:
    encrypted_name = str(uuid.uuid4())
    encrypted_path = os.path.join(ENCRYPTED_DIR, encrypted_name)

    encrypt_file(input_path, encrypted_path, password)
    map_filename(encrypted_name, os.path.basename(input_path))

    return encrypted_path

def decrypt_and_handle(encrypted_path: str, password: str, auto_delete: bool = False) -> bool:
    encrypted_name = os.path.basename(encrypted_path)
    original_name = resolve_original_name(encrypted_name)
    output_path = os.path.join(ENCRYPTED_DIR, original_name)

    success = handle_decryption_attempt(encrypted_path, output_path, password)
    if success and auto_delete:
        delete_after_delay(output_path)

    return success
