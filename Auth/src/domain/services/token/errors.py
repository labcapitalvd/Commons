class TokenError(Exception):
    """Base error class for token service errors"""


class TokenRevoked(TokenError):
    """Token has been revoked"""


class TokenExpired(TokenError):
    """Token is no longer valid"""


class TokenMalformed(TokenError):
    """Token does not contain required claims"""
