import os
from config import LOCK_FILE

def check_lock():
    if os.path.exists(LOCK_FILE):
        print("🔒 This vault is locked due to too many failed attempts.")
        exit(1)

def create_lock():
    with open(LOCK_FILE, "w") as f:
        f.write("LOCKED")
