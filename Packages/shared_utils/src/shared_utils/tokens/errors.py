class TokenError(Exception):
    """Base error for TokenUtils."""

class TokenTypeError(TokenError):
    """Wrong token type error."""
    pass

class TokenExpiredError(TokenError):
    """Expired token error."""
    pass

class TokenEncodeError(TokenError):
    """Token encode error."""
    pass

class TokenDecodeError(TokenError):
    """Token decode error."""
    pass

class CryptoError(Exception):
    """Base error for CryptoUtils."""


class EmptyEncryptionTarget(CryptoError):
    pass
