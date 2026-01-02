class TokenError(Exception):
    """Base error for TokenUtils."""

class InvalidPlatformError(TokenError):
    """Unsupported platform error."""
    pass

class TokenEmptyError(TokenError):
    """Empty token error."""
    pass

class TokenSignatureError(TokenError):
    """Wrong token signature error."""
    pass
    
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
