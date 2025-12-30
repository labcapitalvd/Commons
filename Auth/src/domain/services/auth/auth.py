from shared_utils import get_logger, HashUtils
from shared_models import User

from infrastructure.uow import AuthUnitOfWork

from .errors import InvalidCredentials, UserAlreadyExists


logger = get_logger("api/main")


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
    def __init__(self, uow_factory=AuthUnitOfWork):
        self.uow_factory = uow_factory
        
    async def register(
        self,
        username: str,
        email: str, 
        password: str
    ) -> User:
        """Register user."""
        async with self.uow_factory() as uow:
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
        password: str
    ) -> User:
        """Login user."""
        async with self.uow_factory() as uow:
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
        password: str
    ) -> User:
        """Delete user."""
        async with self.uow_factory() as uow:
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
