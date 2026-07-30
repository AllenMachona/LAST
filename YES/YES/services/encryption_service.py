from cryptography.fernet import Fernet
import os

class EncryptionService:
    def __init__(self):
        self.key = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = self.cipher.encrypt(data)
        enc_path = file_path + '.enc'
        with open(enc_path, 'wb') as f:
            f.write(encrypted)
        return enc_path

    def decrypt_file(self, enc_path):
        with open(enc_path, 'rb') as f:
            data = f.read()
        decrypted = self.cipher.decrypt(data)
        return decrypted
