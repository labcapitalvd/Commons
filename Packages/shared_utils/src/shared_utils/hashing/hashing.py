from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from .contexts import fast_context, token_context, password_context
from .errors import HashError, EmptyHashTarget, HashMismatch, InvalidHashFormat


def hash_value(ctx: CryptContext, value: str) -> str:
    if not value or not value.strip():
        raise EmptyHashTarget("Cannot hash empty string")

    try:
        return ctx.hash(value)
    except Exception as e:
        raise HashError("Hash operation failed") from e


def verify_value(ctx: CryptContext, value: str, hashed_value: str) -> None:
    if not value or not value.strip():
        raise EmptyHashTarget("Cannot verify empty string")
    if not hashed_value or not hashed_value.strip():
        raise EmptyHashTarget("Cannot verify empty string")

    try:
        if not ctx.verify(value, hashed_value):
            raise HashMismatch("Hash verification failed")
    except UnknownHashError as e:
        raise InvalidHashFormat("Unknown or invalid hash format") from e
    except Exception as e:
        raise HashError("Hash operation failed") from e


def hash_password(password: str) -> str:
    """Hashes a password using the password context."""
    return hash_value(password_context, password)
    
def hash_token(token: str) -> str:
    """Hashes a token using the token context."""
    return hash_value(token_context, token)
    
def hash_string(secret: str) -> str:
    """Hashes a string using the fast context."""
    return hash_value(fast_context, secret)


def verify_password(password: str, hashed_password: str) -> None:
    """Verifies a password using the password context."""
    verify_value(password_context, password, hashed_password)

def verify_token(token: str, hashed_token: str) -> None:
    """Verifies a token using the token context."""
    verify_value(token_context, token, hashed_token)

def verify_string(secret: str, hashed_secret: str) -> None:
    """Verifies a string using the fast context."""
    verify_value(fast_context, secret, hashed_secret)
