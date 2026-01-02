from cryptography.fernet import Fernet

from shared_utils.logger import get_logger

from .config import FERNET_KEY
from .errors import EncryptionError, EmptyEncryptionTarget, EmptyDecryptionTarget


logger = get_logger(__name__)
_cipher = Fernet(FERNET_KEY)


def encrypt(text: str) -> str:
    if not text or not text.strip():
        raise EmptyEncryptionTarget("Cannot encrypt empty string")

    try:
        return _cipher.encrypt(text.encode()).decode()
    except Exception as e:
        raise EncryptionError("Encryption failed") from e


def decrypt(token: str) -> str:
    if not token or not token.strip():
        raise EmptyDecryptionTarget("Cannot decrypt empty string")

    try:
        return _cipher.decrypt(token.encode()).decode()
    except Exception as e:
        raise EncryptionError("Decryption failed") from e