from cryptography.fernet import Fernet

# Generate encryption key (run once and save the key)
def generate_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open('key.key', 'rb').read()

# Encrypt the password
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

# Decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()
