from typing import Optional
from cryptography.fernet import Fernet

from shared_utils.encryption.errors import CryptoError, EmptyEncryptionTarget


class CryptoUtils:
    def __init__(self, key: Optional[bytes] = None):
        if key is None:
            # Generate a key once and store it securely
            key = Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt(self, text: str) -> str:
        """Encrypt the given text."""
        if not text or text.strip() == "":
            raise EmptyEncryptionTarget("Cannot encrypt empty string")
        try:
            encrypted = self.cipher.encrypt(text.encode("utf-8"))
            return encrypted.decode()
        except Exception as e:
            raise CryptoError(f"Encryption failed: {e}")

    def decrypt(self, token: str) -> str:
        """Decrypt the given encrypted text."""
        if not token or token.strip() == "":
            raise EmptyEncryptionTarget("Cannot decrypt empty string")
        try:
            decrypted = self.cipher.decrypt(token.encode("utf-8"))
            return decrypted.decode()
        except Exception as e:
            raise CryptoError(f"Encryption failed: {e}")
