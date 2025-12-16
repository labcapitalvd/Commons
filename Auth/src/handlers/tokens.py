import os
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid7

from sqlalchemy.ext.asyncio import AsyncSession

from joserfc import jwt, jws
from joserfc.jwk import OKPKey
from joserfc.errors import JoseError, InsecureClaimError

from db.tokens import TokenDb

from handlers.errors import (
    TokenEncodeError,
)

from shared_utils.tokens import TokenChecker


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
    raise FileNotFoundError(f"JWT_PRIVATE_KEY_FILE file not found at {JWT_PRIVATE_KEY_FILE}")
with open(JWT_PRIVATE_KEY_FILE, "rb") as f:
    JWT_PRIVATE_KEY = OKPKey.import_key(f.read())

logger = logging.getLogger("seed/users")
logger.setLevel(LOGLEVEL)

registry = jws.JWSRegistry(algorithms=[JWT_ASYMETRIC_ALGORITHM])

class TokenIssuer:
    @staticmethod
    def generate_token(
        user_id: UUID, username: str, token_type: str = "access"
    ) -> str:
        """
        Generate either an access or refresh token.
        token_type: "access" | "refresh"
        """
        try:
            now = datetime.now(timezone.utc)

            expire_minutes = (
                JWT_EXPIRE_MINUTES_ACCESS
                if token_type == "access"
                else JWT_EXPIRE_MINUTES_REFRESH
            )
            exp = now + timedelta(minutes=expire_minutes)
            
            header = {
                "typ": "JWT",
                "alg": "EdDSA"
            }

            claims = {
                "sub": str(user_id),
                "username": username,
                "token_type": token_type,
                "iat": int(now.timestamp()),
                "exp": int(exp.timestamp()),
            }

            if token_type == "refresh":
                claims["jti"] = str(uuid7())
            return jwt.encode(header, claims, JWT_PRIVATE_KEY, registry=registry)
        
        except InsecureClaimError:
            raise TokenEncodeError("Insecure claim error")
        
        except JoseError as e:
            logger.error(f"Error encoding {token_type} token: {e}")
            raise TokenEncodeError(f"Error encoding {token_type} token: {e}")


class TokenHandler:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tokenondb = TokenDb(self.db)
        self.token_issuer = TokenIssuer()
        self.token_checker = TokenChecker()

    async def issue_tokens(self, user_id: UUID, username: str):
        """Generate access and refresh tokens"""
        access_token = self.token_issuer.generate_token(
            user_id, username, "access"
        )
        refresh_token = self.token_issuer.generate_token(
            user_id, username, "refresh"
        )

        await self.tokenondb.create_refresh_token_entry(refresh_token)

        return access_token, refresh_token

    async def reauth(self, old_refresh_token: str) -> tuple[str, str]:
        """Invalidate old refresh token and issue new tokens."""
        # Decode old refresh token
        dec = self.token_checker.decode_token(old_refresh_token, "refresh")
        decoded = dec.claims
        
        user_id = UUID(decoded["sub"])
        username = decoded["username"]

        await self.tokenondb.delete_refresh_token_entry(old_refresh_token)

        return await self.issue_tokens(user_id, username)

    async def logout(self, refresh_token: str) -> None:
        """Invalidate refresh token only."""
        await self.tokenondb.delete_refresh_token_entry(refresh_token)
