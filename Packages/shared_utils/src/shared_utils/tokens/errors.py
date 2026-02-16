class TokenError(Exception):
    """Base error for TokenUtils."""


class InvalidPlatformError(TokenError):
    """Unsupported platform error."""


class TokenEmptyError(TokenError):
    """Empty token error."""


class TokenSignatureError(TokenError):
    """Wrong token signature error."""


class TokenTypeError(TokenError):
    """Wrong token type error."""


class TokenExpiredError(TokenError):
    """Expired token error."""


class TokenEncodeError(TokenError):
    """Token encode error."""


class TokenDecodeError(TokenError):
    """Token decode error."""
