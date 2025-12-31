class AuthError(Exception):
    pass

class TierDoesntExist(AuthError):
    """Default user tier not found, cannot register user"""


class InvalidCredentials(AuthError):
    """Username or password is incorrect"""


class UserAlreadyExists(AuthError):
    """User already exists"""


class UserDisabled(AuthError):
    """User exists but cannot authenticate"""


class TokenRevoked(AuthError):
    """Token is no longer valid"""
