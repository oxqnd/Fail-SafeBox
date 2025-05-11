import os
import time

def delete_after_delay(path: str, delay: int = 5):
    print(f"🕒 Auto-deleting {path} in {delay} seconds...")
    time.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
        print("💣 Decrypted file auto-deleted.")
