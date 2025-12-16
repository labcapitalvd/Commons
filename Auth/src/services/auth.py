import os
import logging
from uuid import UUID

from pydantic import SecretStr

from sqlalchemy.ext.asyncio import AsyncSession

from handlers.users import UserHandler
from handlers.tokens import TokenHandler

from shared_utils.tokens import TokenChecker


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
    def __init__(self, db: AsyncSession):
        self.auth = UserHandler(db)
        self.tokens = TokenHandler(db)
        self.tokenchecker = TokenChecker()

    async def login_with_tokens(
        self, username: str, password: SecretStr
    ) -> tuple[str, str]:
        """Login user and issue tokens."""
        try:
            user = await self.auth.login_user(username, password)
            if not user:
                logger.error(f"User error: {username}")
                raise 
            return await self.tokens.issue_tokens(user.id, user.username)
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise 
    async def rotate_tokens(self, old_refresh_token: str) -> tuple[str, str]:
        """Re-authenticate and issue new tokens."""
        try:
            dec = self.tokenchecker.decode_token(
                old_refresh_token,
                "refresh"
            )
            decoded = dec.claims
            user_id = UUID(decoded["sub"])

            user = await self.auth.get_user(user_id)
            if not user:
                logger.error(f"User error: {user_id}")
                raise 
            return await self.tokens.reauth(old_refresh_token)
        except Exception as e:
            logger.error(f"Error rotating tokens: {e}")
            raise
    async def logout_user(self, refresh_token: str):
        """Invalidate refresh token."""
        try:
            dec = self.tokenchecker.decode_token(
                refresh_token,
                "refresh"
            )
            decoded = dec.claims
            user_id = UUID(decoded["sub"])

            user = await self.auth.get_user(user_id)
            if not user:
                logger.error(f"User error: {refresh_token}")
                raise
            await self.tokens.logout(refresh_token)
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            raise