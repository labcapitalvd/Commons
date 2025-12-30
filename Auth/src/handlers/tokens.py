import os
from uuid import UUID

from joserfc.jwk import OKPKey
from sqlalchemy.ext.asyncio import AsyncSession

from shared_utils import get_logger, TokenIssuer, TokenVerifier

from db.tokens import TokenDb


LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)
JWT_ASYMETRIC_ALGORITHM = os.environ["JWT_ASYMETRIC_ALGORITHM"]
JWT_EXPIRE_MINUTES_ACCESS = int(os.environ["JWT_EXPIRE_MINUTES_ACCESS"])
JWT_EXPIRE_MINUTES_REFRESH = int(os.environ["JWT_EXPIRE_MINUTES_REFRESH"])

JWT_PRIVATE_KEY_FILE = "/run/secrets/jwt_private_key"
if not os.path.exists(JWT_PRIVATE_KEY_FILE):
    raise FileNotFoundError(
        f"JWT_PRIVATE_KEY_FILE file not found at {JWT_PRIVATE_KEY_FILE}"
    )
with open(JWT_PRIVATE_KEY_FILE, "rb") as f:
    JWT_PRIVATE_KEY = OKPKey.import_key(f.read())

logger = get_logger("seed/users")


class TokenHandler:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tokenondb = TokenDb(self.db)

    async def issue_tokens(self, user_id: UUID, username: str):
        """Generate access and refresh tokens"""
        access_token = TokenIssuer.generate_token(user_id, username, "access")
        refresh_token = TokenIssuer.generate_token(user_id, username, "refresh")

        await self.tokenondb.create_refresh_token_entry(refresh_token)

        return access_token, refresh_token

    async def reauth(self, old_refresh_token: str) -> tuple[str, str]:
        """Invalidate old refresh token and issue new tokens."""
        # Decode old refresh token
        dec = TokenVerifier.decode_token(old_refresh_token, "refresh")
        decoded = dec.claims

        user_id = UUID(decoded["sub"])
        username = decoded["username"]

        self.tokenondb.delete_refresh_token_entry(old_refresh_token)

        return await self.issue_tokens(user_id, username)

    async def logout(self, refresh_token: str) -> None:
        """Invalidate refresh token only."""
        self.tokenondb.delete_refresh_token_entry(refresh_token)
