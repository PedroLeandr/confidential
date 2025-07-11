import os
import sys
import random
from cryptography.fernet import Fernet

def resolve_lnk(path):
    if not path.lower().endswith(".lnk"):
        return path
    try:
        import pylnk3
        with open(path, 'rb') as f:
            lnk = pylnk3.parse(f)
            return lnk.link_info.local_base_path
    except Exception as e:
        print(f"❌ Failed to resolve .lnk: {e}")
        sys.exit(1)

def generate_key(folder_path):
    key = Fernet.generate_key()
    with open(os.path.join(folder_path, "key.key"), "wb") as f:
        f.write(key)
    return key

def load_key(folder_path):
    key_path = os.path.join(folder_path, "key.key")
    if not os.path.exists(key_path):
        print("❌ Key file not found.")
        sys.exit(1)
    with open(key_path, "rb") as f:
        return f.read()

def generate_code(folder_path, key):
    code = ''.join(random.choices("0123456789", k=8))
    fernet = Fernet(key)
    with open(os.path.join(folder_path, "code.lock"), "wb") as f:
        f.write(fernet.encrypt(code.encode()))
    return code

def validate_code(folder_path, key, input_code):
    code_path = os.path.join(folder_path, "code.lock")
    if not os.path.exists(code_path):
        print("❌ Code file not found.")
        sys.exit(1)
    fernet = Fernet(key)
    with open(code_path, "rb") as f:
        encrypted_code = f.read()
    try:
        real_code = fernet.decrypt(encrypted_code).decode()
        return real_code == input_code
    except:
        return False

def encrypt_folder(folder_path, key):
    fernet = Fernet(key)
    errors = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name in ("key.key", "code.lock"):
                continue
            full_path = os.path.join(root, name)
            print(f"🔒 Encrypting: {full_path}")
            try:
                with open(full_path, "rb") as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                with open(full_path, "wb") as f:
                    f.write(encrypted_data)
            except Exception as e:
                errors.append((full_path, str(e)))
    print("✅ Folder encrypted.")
    if errors:
        print("\n⚠️ Errors during encryption:")
        for path, err in errors:
            print(f" - {path}: {err}")

def decrypt_folder(folder_path, key):
    fernet = Fernet(key)
    errors = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            if name in ("key.key", "code.lock"):
                continue
            full_path = os.path.join(root, name)
            print(f"🔓 Decrypting: {full_path}")
            try:
                with open(full_path, "rb") as f:
                    data = f.read()
                decrypted_data = fernet.decrypt(data)
                with open(full_path, "wb") as f:
                    f.write(decrypted_data)
            except Exception as e:
                errors.append((full_path, str(e)))
    print("✅ Folder decrypted.")
    if errors:
        print("\n⚠️ Errors during decryption:")
        for path, err in errors:
            print(f" - {path}: {err}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python encrypter.py encrypt path_to_folder_or_lnk")
        print("  python encrypter.py decrypt path_to_folder_or_lnk")
        sys.exit(1)

    action = sys.argv[1]
    input_path = sys.argv[2]
    folder = resolve_lnk(input_path)

    if not os.path.isdir(folder):
        print("❌ Invalid folder path.")
        sys.exit(1)

    if action == "encrypt":
        key = generate_key(folder)
        code = generate_code(folder, key)
        encrypt_folder(folder, key)
        print(f"\n🧠 SAVE THIS CODE: {code} 🔐\n")

    elif action == "decrypt":
        key = load_key(folder)
        code = input("🔑 Enter your 8-digit code: ").strip()
        if not code.isdigit() or len(code) != 8:
            print("❌ Invalid code format.")
            sys.exit(1)
        if not validate_code(folder, key, code):
            print("❌ Incorrect code.")
            sys.exit(1)
        decrypt_folder(folder, key)

    else:
        print("❌ Invalid action. Use 'encrypt' or 'decrypt'.")
