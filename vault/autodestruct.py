import os
import json
from datetime import datetime
from config import MAX_FAIL_COUNT, LOG_PATH
from .crypto import decrypt_file

def load_log() -> list:
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_log(log: list):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def log_attempt(success: bool):
    log = load_log()
    log.append({
        "timestamp": datetime.now().isoformat(),
        "success": success
    })
    save_log(log)

def count_failures(log: list) -> int:
    return sum(1 for entry in reversed(log) if not entry["success"])

def destroy_file(path: str):
    if not os.path.exists(path):
        return
    size = os.path.getsize(path)
    with open(path, "wb") as f:
        f.write(os.urandom(size))
    os.remove(path)
    print("💥 File has been securely destroyed due to too many failed attempts.")

def handle_decryption_attempt(input_path: str, output_path: str, password: str) -> bool:
    log = load_log()
    failure_count = count_failures(log)

    if failure_count >= MAX_FAIL_COUNT:
        destroy_file(input_path)
        return False

    success = decrypt_file(input_path, output_path, password)
    log_attempt(success)

    if not success:
        failure_count += 1
        if failure_count >= MAX_FAIL_COUNT:
            destroy_file(input_path)

    return success
