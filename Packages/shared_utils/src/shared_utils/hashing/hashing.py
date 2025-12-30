from passlib.context import CryptContext

from .contexts import fast_context, token_context, password_context
from .errors import HashError, EmptyHashTarget


class HashUtils:
    @staticmethod
    def _hash(ctx: CryptContext, value: str) -> str:
        if not value or value.strip() == "":
            raise EmptyHashTarget("Cannot hash empty string")
        try:
            return ctx.hash(value)
        except Exception as e:
            raise HashError(e)

    @staticmethod
    def _verify(ctx: CryptContext, value: str, hashed: str) -> bool:
        if not value or value.strip() == "":
            raise EmptyHashTarget("Cannot verify empty string")
        if not hashed or hashed.strip() == "":
            raise EmptyHashTarget("Cannot verify empty string")
        try:
            return ctx.verify(value, hashed)
        except Exception as e:
            raise HashError(e)

    # ---- public API ----

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._hash(password_context, password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        return cls._verify(password_context, password, hashed)

    @classmethod
    def hash_token(cls, token: str) -> str:
        return cls._hash(token_context, token)

    @classmethod
    def verify_token(cls, token: str, hashed: str) -> bool:
        return cls._verify(token_context, token, hashed)

    @classmethod
    def hash_fast(cls, secret: str) -> str:
        return cls._hash(fast_context, secret)

    @classmethod
    def verify_fast(cls, secret: str, hashed: str) -> bool:
        return cls._verify(fast_context, secret, hashed)
