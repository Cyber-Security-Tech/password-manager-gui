"""
encryption.py – Handles symmetric encryption and decryption of sensitive data.

Uses Fernet (AES 128 in CBC mode with HMAC) from the cryptography library.
Automatically generates a key if one is not provided.
"""

from cryptography.fernet import Fernet

class Encryptor:
    """
    Provides methods to encrypt and decrypt strings using Fernet symmetric encryption.
    """

    def __init__(self, key=None):
        """
        Initializes the encryptor.

        If no key is provided, a new key is generated.
        In production, the key should be securely stored and retrieved.
        """
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """
        Encrypts a plaintext string and returns a base64-encoded ciphertext string.
        """
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        """
        Decrypts a base64-encoded ciphertext string and returns the original plaintext.
        """
        return self.cipher.decrypt(data.encode()).decode()
