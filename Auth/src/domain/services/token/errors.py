class AuthError(Exception):
    pass


class InvalidCredentials(AuthError):
    """Username or password is incorrect"""


class UserAlreadyExists(AuthError):
    """User already exists"""


class UserDisabled(AuthError):
    """User exists but cannot authenticate"""


class TokenError(AuthError):
    """Token has an error"""


class TokenRevoked(AuthError):
    """Token has been revoked"""


class TokenExpired(AuthError):
    """Token is no longer valid"""
