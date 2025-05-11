import os
import json
from config import MAPPING_FILE

def load_mapping():
    if not os.path.exists(MAPPING_FILE):
        return {}
    with open(MAPPING_FILE, "r") as f:
        return json.load(f)

def save_mapping(mapping):
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

def map_filename(encrypted_name, original_name):
    mapping = load_mapping()
    mapping[encrypted_name] = original_name
    save_mapping(mapping)

def resolve_original_name(encrypted_name):
    mapping = load_mapping()
    return mapping.get(encrypted_name, "decrypted.txt")
