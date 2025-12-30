class AuthError(Exception):
    pass


class InvalidCredentials(AuthError):
    """Username or password is incorrect"""


class UserAlreadyExists(AuthError):
    """User already exists"""


class UserDisabled(AuthError):
    """User exists but cannot authenticate"""


class TokenError(AuthError):
    """Token is no longer valid"""

class TokenRevoked(AuthError):
    """Token is no longer valid"""

class TokenInvalid(AuthError):
    """Token is no longer valid"""
