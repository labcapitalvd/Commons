class EncryptionError(Exception):
    """Base error for EncryptionUtils."""

class EmptyEncryptionTarget(EncryptionError):
    pass

class EmptyDecryptionTarget(EncryptionError):
    pass
