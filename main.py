import sys
import getpass
from vault.lock import check_lock
from vault.operations import encrypt_and_map, decrypt_and_handle

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py [encrypt|decrypt] <file_path> [--autodelete]")
        return

    command = sys.argv[1]
    file_path = sys.argv[2]
    auto_delete = "--autodelete" in sys.argv

    check_lock()
    password = getpass.getpass("Enter password: ")

    if command == "encrypt":
        path = encrypt_and_map(file_path, password)
        print(f"✅ File encrypted and saved as: {path}")
    elif command == "decrypt":
        if decrypt_and_handle(file_path, password, auto_delete):
            print("✅ Decryption successful.")
        else:
            print("❌ Decryption failed or file destroyed.")
    else:
        print("Unknown command:", command)

if __name__ == "__main__":
    main()
