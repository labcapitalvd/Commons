class TokenError(Exception):
    """Base error for TextUtils."""

class TokenTypeError(TokenError):
    pass

class TokenExpiredError(TokenError):
    pass

class TokenEncodeError(TokenError):
    pass

class TokenDecodeError(TokenError):
    pass

class CryptoError(Exception):
    """Base error for CryptoUtils."""


class EmptyEncryptionTarget(CryptoError):
    pass
