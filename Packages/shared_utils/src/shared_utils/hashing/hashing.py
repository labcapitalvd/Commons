from passlib.context import CryptContext

from shared_utils.hashing.errors import HashError, EmptyHashTarget


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class HashUtils:
    @staticmethod
    def hash_string(password: str) -> str:
        """Hashes a password using bcrypt"""
        if not password or password.strip() == "":
            raise EmptyHashTarget("Cannot encrypt empty string")
        try:
            return pwd_context.hash(password)
        except Exception as e:
            raise HashError(e)

    @staticmethod
    def verify_hash(password: str, hashed_password: str) -> bool:
        """Verifies a hashed password"""
        if not password or password.strip() == "":
            raise EmptyHashTarget("Cannot decrypt empty string")
        if not hashed_password or hashed_password.strip() == "":
            raise EmptyHashTarget("Cannot decrypt empty string")
        try:
            return pwd_context.verify(password, hashed_password)
        except Exception as e:
            raise HashError(e)
