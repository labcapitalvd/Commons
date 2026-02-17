class AuthError(Exception):
    """Base error for auth service errors"""


class TierDoesntExist(AuthError):
    """Default user tier not found, cannot register user"""


class InvalidCredentials(AuthError):
    """Username or password is incorrect"""


class UserAlreadyExists(AuthError):
    """User already exists"""

