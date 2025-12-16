class CryptoError(Exception):
    """Base error for CryptoUtils."""


class EmptyEncryptionTarget(CryptoError):
    pass
