class EncryptionError(Exception):
    """Base error for EncryptionUtils."""


class DecryptionError(Exception):
    """Base error for DecryptionUtils."""


class EmptyEncryptionTarget(EncryptionError):
    pass


class EmptyDecryptionTarget(DecryptionError):
    pass
