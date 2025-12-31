from typing import Optional
from uuid import UUID

from pydantic import EmailStr, SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import User
from shared_utils.logging import get_logger
from shared_utils import HashUtils, TextUtils

from db.users import UsersDb


logger = get_logger("seed/users")


class UserHandler:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.userondb = UsersDb(self.db)
        self.textutils = TextUtils()

    async def get_user(self, id: UUID) -> Optional[User]:
        try:
            dup = await self.userondb.get_user_entry(id=id)
            if dup:
                return dup
            else:
                return None

        except Exception as e:
            logger.error(f"Getting user failed on handler: {e}")
            raise

    async def register_user(
        self, username_api: str, email_api: EmailStr, password_api: SecretStr
    ) -> Optional[User]:
        try:
            username = self.textutils.sanitize_text(username_api)
            email = self.textutils.is_valid_and_safe_email(email_api)
            password = self.textutils.sanitize_text(password_api.get_secret_value())

            dup = await self.userondb.get_user_entry(username=username)
            if not dup:
                return await self.userondb.create_user_entry(username, email, password)

            return None

        except Exception as e:
            logging.error(f"Registration failed on handler: {str(e)}")
            raise

    async def login_user(
        self, username_api: str, password_api: SecretStr
    ) -> Optional[User]:
        try:
            username = self.textutils.sanitize_text(username_api)
            password = self.textutils.sanitize_text(password_api.get_secret_value())

            user = await self.userondb.get_user_entry(username=username)

            stored_hash = user.password_hash if user else "$2b$12$" + "a" * 53
            password_matches = HashUtils.verify_hash(password, stored_hash)

            if user and password_matches:
                return user

            return None
        except Exception as e:
            logging.error(f"Login failed on handler: {str(e)}")
            raise

    async def delete_user(
        self, username_api: str, email_api: EmailStr, password_api: SecretStr
    ) -> bool:
        try:
            username = self.textutils.sanitize_text(username_api)
            password = self.textutils.sanitize_text(password_api.get_secret_value())
            email = self.textutils.is_valid_and_safe_email(email_api)

            return await self.userondb.delete_user_entry(
                username=username, email=email, passwd=password
            )
        except Exception as e:
            logging.error(f"Delete failed on handler: {str(e)}")
            raise

    async def update_username(self, current_user: UUID, username_api: str) -> bool:
        try:
            username = self.textutils.sanitize_text(username_api)

            await self.userondb.update_user_entry(
                id=current_user, new_username=username
            )
            return True
        except Exception as e:
            logging.error(f"Update failed on username update: {str(e)}")
            raise

    async def update_email(self, current_user: UUID, email_api: EmailStr) -> bool:
        try:
            email = self.textutils.is_valid_and_safe_email(email_api)

            await self.userondb.update_user_entry(id=current_user, new_email=email)
            return True
        except Exception as e:
            logging.error(f"Update failed on email update: {str(e)}")
            raise

    async def update_password(
        self, current_user: UUID, password_api: SecretStr
    ) -> bool:
        try:
            password = self.textutils.sanitize_text(password_api.get_secret_value())

            await self.userondb.update_user_entry(
                id=current_user, new_password=password
            )
            return True
        except Exception as e:
            logging.error(f"Update failed on password update: {str(e)}")
            raise
