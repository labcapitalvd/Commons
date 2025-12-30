
from encodings.mac_arabic import IncrementalDecoder
import os
import logging
from uuid import UUID

from pydantic import SecretStr, EmailStr

from sqlalchemy.ext.asyncio import AsyncSession

from shared_utils import HashUtils
from shared_models import User

from infrastructure.uow import AuthUnitOfWork
from .errors import AuthError, InvalidCredentials, UserAlreadyExists


DUMMY_HASH = HashUtils.hash_string("this-value-does-not-matter")

LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)

logger = logging.getLogger("api/main")
logger.setLevel(LOGLEVEL)


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
            
            user = User(
                username=username,
                email=email,
                password_hash=HashUtils.hash_string(password)
            )
            
            await uow.users.add_user(user)
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
            if not HashUtils.verify_hash(password, stored_hash):
                raise InvalidCredentials("Invalid credentials")
            
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
            if not HashUtils.verify_hash(password, stored_hash):
                raise InvalidCredentials("Invalid credentials")

        await uow.users.delete_user(user)
        return user





# class AuthService:
#     def __init__(self, db: AsyncSession):
#         self.auth = UserHandler(db)
#         self.tokens = TokenHandler(db)
#         self.tokenchecker = TokenChecker()

#     async def login_with_tokens(
#         self, username: str, password: SecretStr
#     ) -> tuple[str, str]:
#         """Login user and issue tokens."""
#         try:
#             user = await self.auth.login_user(username, password)
#             if not user:
#                 logger.error(f"User error: {username}")
#                 raise 
#             return await self.tokens.issue_tokens(user.id, user.username)
#         except Exception as e:
#             logger.error(f"Login error: {e}")
#             raise 
#     async def rotate_tokens(self, old_refresh_token: str) -> tuple[str, str]:
#         """Re-authenticate and issue new tokens."""
#         try:
#             dec = self.tokenchecker.decode_token(
#                 old_refresh_token,
#                 "refresh"
#             )
#             decoded = dec.claims
#             user_id = UUID(decoded["sub"])

#             user = await self.auth.get_user(user_id)
#             if not user:
#                 logger.error(f"User error: {user_id}")
#                 raise 
#             return await self.tokens.reauth(old_refresh_token)
#         except Exception as e:
#             logger.error(f"Error rotating tokens: {e}")
#             raise
#     async def logout_user(self, refresh_token: str):
#         """Invalidate refresh token."""
#         try:
#             dec = self.tokenchecker.decode_token(
#                 refresh_token,
#                 "refresh"
#             )
#             decoded = dec.claims
#             user_id = UUID(decoded["sub"])

# class AuthService:
#     def __init__(self, db: AsyncSession):
#         self.auth = UserHandler(db)
#         self.tokens = TokenHandler(db)
#         self.tokenchecker = TokenChecker()

#     async def login_with_tokens(
#         self, username: str, password: SecretStr
#     ) -> tuple[str, str]:
#         """Login user and issue tokens."""
#         try:
#             user = await self.auth.login_user(username, password)
#             if not user:
#                 logger.error(f"User error: {username}")
#                 raise 
#             return await self.tokens.issue_tokens(user.id, user.username)
#         except Exception as e:
#             logger.error(f"Login error: {e}")
#             raise 
#     async def rotate_tokens(self, old_refresh_token: str) -> tuple[str, str]:
#         """Re-authenticate and issue new tokens."""
#         try:
#             dec = self.tokenchecker.decode_token(
#                 old_refresh_token,
#                 "refresh"
#             )
#             decoded = dec.claims
#             user_id = UUID(decoded["sub"])

#             user = await self.auth.get_user(user_id)
#             if not user:
#                 logger.error(f"User error: {user_id}")
#                 raise 
#             return await self.tokens.reauth(old_refresh_token)
#         except Exception as e:
#             logger.error(f"Error rotating tokens: {e}")
#             raise
#     async def logout_user(self, refresh_token: str):
#         """Invalidate refresh token."""
#         try:
#             dec = self.tokenchecker.decode_token(
#                 refresh_token,
#                 "refresh"
#             )
#             decoded = dec.claims
#             user_id = UUID(decoded["sub"])

#             user = await self.auth.get_user(user_id)
#             if not user:
#                 logger.error(f"User error: {refresh_token}")
#                 raise
#             await self.tokens.logout(refresh_token)
#         except Exception as e:
#             logger.error(f"Error logging out user: {e}")
#             raise
            
            
# class AuthService:
            
#     def __init__(self, db: AsyncSession):
#         self.db = db
#         self.userondb = UsersDb(self.db)
#         self.textutils = TextUtils()

#     async def get_user(self, id: UUID) -> Optional[User]:
#         try:
#             dup = await self.userondb.get_user_entry(id=id)
#             if dup:
#                 return dup
#             else:
#                 return None

#         except Exception as e:
#             logger.error(f"Getting user failed on handler: {e}")
#             raise 

#     async def register_user(
#         self, username_api: str, email_api: EmailStr, password_api: SecretStr
#     ) -> Optional[User]:
#         try:
#             username = self.textutils.sanitize_text(username_api)
#             email = self.textutils.is_valid_and_safe_email(email_api)
#             password = self.textutils.sanitize_text(password_api.get_secret_value())

#             dup = await self.userondb.get_user_entry(username=username)
#             if not dup:
#                 return await self.userondb.create_user_entry(username, email, password)

#             return None

#         except Exception as e:
#             logging.error(f"Registration failed on handler: {str(e)}")
#             raise 

#     async def login_user(
#         self, username_api: str, password_api: SecretStr
#     ) -> Optional[User]:
#         try:
#             username = self.textutils.sanitize_text(username_api)
#             password = self.textutils.sanitize_text(password_api.get_secret_value())

#             user = await self.userondb.get_user_entry(username=username)

#             stored_hash = user.password_hash if user else "$2b$12$" + "a" * 53
#             password_matches = HashUtils.verify_hash(password, stored_hash)

#             if user and password_matches:
#                 return user

#             return None
#         except Exception as e:
#             logging.error(f"Login failed on handler: {str(e)}")
#             raise 

#     async def delete_user(
#         self, username_api: str, email_api: EmailStr, password_api: SecretStr
#     ) -> bool:
#         try:
#             username = self.textutils.sanitize_text(username_api)
#             password = self.textutils.sanitize_text(password_api.get_secret_value())
#             email = self.textutils.is_valid_and_safe_email(email_api)

#             return await self.userondb.delete_user_entry(
#                 username=username, email=email, passwd=password
#             )
#         except Exception as e:
#             logging.error(f"Delete failed on handler: {str(e)}")
#             raise 

#     async def update_username(self, current_user: UUID, username_api: str) -> bool:
#         try:
#             username = self.textutils.sanitize_text(username_api)

#             await self.userondb.update_user_entry(
#                 id=current_user, new_username=username
#             )
#             return True
#         except Exception as e:
#             logging.error(f"Update failed on username update: {str(e)}")
#             raise 

#     async def update_email(self, current_user: UUID, email_api: EmailStr) -> bool:
#         try:
#             email = self.textutils.is_valid_and_safe_email(email_api)

#             await self.userondb.update_user_entry(id=current_user, new_email=email)
#             return True
#         except Exception as e:
#             logging.error(f"Update failed on email update: {str(e)}")
#             raise 

#     async def update_password(
#         self, current_user: UUID, password_api: SecretStr
#     ) -> bool:
#         try:
#             password = self.textutils.sanitize_text(password_api.get_secret_value())

#             await self.userondb.update_user_entry(
#                 id=current_user, new_password=password
#             )
#             return True
#         except Exception as e:
#             logging.error(f"Update failed on password update: {str(e)}")
#             raise 
