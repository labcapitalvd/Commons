from shared_utils import HashUtils
from shared_models import User

from infrastructure.uow import AuthUoW

from .errors import InvalidCredentials, UserAlreadyExists


class AuthCrypto:
    @staticmethod
    def hash_password(raw: str) -> str:
        try:
            return HashUtils.hash_password(raw)
        except Exception as e:
            raise RuntimeError("Failed to hash password") from e

    @staticmethod
    def verify_password(raw: str, hashed: str) -> bool:
        try:
            return HashUtils.verify_password(raw, hashed)
        except Exception:
            return False


DUMMY_HASH = AuthCrypto.hash_password("this-value-does-not-matter")


class AuthService:        
    async def register(
        self,
        username: str,
        email: str, 
        password: str,
        uow: AuthUoW,
    ) -> User:
        """Register user."""
        if await uow.users.get_by_username(username):
            raise UserAlreadyExists()
        
        password_hash = AuthCrypto.hash_password(password)
        
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        uow.users.add_user(user)
        return user


    async def login(
        self, 
        username: str, 
        password: str,
        uow: AuthUoW,
    ) -> User:
        """Login user."""
        user = await uow.users.get_by_username(username)
        
        if not user:
            raise InvalidCredentials("Invalid credentials")
        
        stored_hash = user.password_hash if user else DUMMY_HASH
        if not AuthCrypto.verify_password(
            password,
            stored_hash
        ):
            raise InvalidCredentials()
        
        return user


    async def delete_account(
        self, 
        username: str, 
        password: str,
        uow: AuthUoW,
    ) -> User:
        """Delete user."""
        user = await uow.users.get_by_username(username)
        
        if not user:
            raise InvalidCredentials("Invalid credentials")
        
        stored_hash = user.password_hash if user else DUMMY_HASH
        if not AuthCrypto.verify_password(
            password,
            stored_hash
        ):
            raise InvalidCredentials()

        uow.users.delete_user(user)
        return user
