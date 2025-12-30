import os
import logging
from uuid import UUID
from datetime import datetime, timezone


from shared_utils import HashUtils
from shared_models import RefreshSession

from utils.tokens import TokenIssuer
from shared_utils import TokenVerifier

from infrastructure.uow import AuthUnitOfWork


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


class TokenService:    
    @staticmethod
    async def issue_tokens(
        user_id: UUID, 
        username: str, 
        uow: AuthUnitOfWork
    ) -> tuple[str, str]:
        """Generate access and refresh tokens"""
        access_token, _, _ = TokenIssuer.generate_token(user_id, username, "access")
        refresh_token, expr, jti = TokenIssuer.generate_token(user_id, username, "refresh")
        
        if jti is None:
            raise ValueError("Refresh token must have a jti")
        
        db_token = RefreshSession(
            jti = jti,
            user_id = user_id,
            refresh_hash = HashUtils.hash_string(refresh_token),
            expires_at=datetime.fromtimestamp(expr, tz=timezone.utc)
        )
        
        await uow.tokens.create_refresh_token(db_token)
        return access_token, refresh_token

    @staticmethod
    async def reauth(
        old_refresh_token: str,
        uow: AuthUnitOfWork
    ) -> tuple[str, str]:
        """Invalidate old refresh token and issue new tokens."""
            
        dec = TokenVerifier.decode_token(old_refresh_token, "refresh")
        decoded = dec.claims
        
        user_id = UUID(decoded["sub"])
        username = decoded["username"]
        jti = decoded["jti"]
        
        old_token = await uow.tokens.get_refresh_token_by_jti(jti)
        if old_token:
            await uow.tokens.delete_refresh_token(old_token)

        return await self.issue_tokens(user_id, username, uow=uow)

    @staticmethod
    async def logout(
        refresh_token: str,
        uow: AuthUnitOfWork
    ) -> None:
        """Invalidate refresh token only."""
        dec = TokenVerifier.decode_token(refresh_token, "refresh")
        decoded = dec.claims
        jti = decoded["jti"]
        
        old_token = await uow.tokens.get_refresh_token_by_jti(jti)
        if old_token:
            await uow.tokens.delete_refresh_token(old_token)
