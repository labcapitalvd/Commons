from uuid import UUID
from datetime import datetime, timezone

from shared_models import RefreshSession
from shared_utils.tokens import generate_token, decode_token
from shared_utils.hashing import hash_token, verify_token

from infrastructure.uow import AuthUoW

from shared_utils import get_logger
from .errors import TokenRevoked, TokenInvalid


logger = get_logger(__name__)


class TokenService:
    async def issue_tokens(
        self, user_id: UUID, username: str, uow: AuthUoW
    ) -> tuple[str, str]:
        """Generate access and refresh tokens"""
        client_access_token, _, _ = generate_token(user_id, username, "access")
        client_refresh_token, expr, jti = generate_token(user_id, username, "refresh")

        if jti is None:
            raise ValueError("Refresh token must have a jti")

        refresh_hash = hash_token(token=client_refresh_token)

        db_token = RefreshSession(
            jti=jti,
            user_id=user_id,
            refresh_hash=refresh_hash,
            expires_at=datetime.fromtimestamp(expr, tz=timezone.utc),
        )

        uow.tokens.create_refresh_token(db_token)
        return client_access_token, client_refresh_token

    async def reauth(self, client_refresh_token: str, uow: AuthUoW) -> tuple[str, str]:
        """Invalidate old refresh token and issue new tokens."""

        dec = decode_token(client_refresh_token, "refresh")
        decoded = dec.claims
        jti = decoded["jti"]
        user = decoded["sub"]

        db_token = await uow.tokens.get_refresh_token_by_jti(user_id=user, jti=jti)
        if not db_token:
            logger.warning(
                "Attempt to use revoked refresh token on reauth: jti=%s", jti
            )
            raise TokenRevoked()

        try:
            verify_token(token=client_refresh_token, hashed_token=db_token.refresh_hash)
        except Exception as e:
            logger.warning(
                "Failed to verify refresh token on reauth: jti=%s, reason=%s", jti, e
            )
            raise TokenInvalid() from e

        uow.tokens.delete_refresh_token(db_token)

        return await self.issue_tokens(
            UUID(decoded["sub"]), decoded["username"], uow=uow
        )

    async def logout(self, client_refresh_token: str, uow: AuthUoW) -> None:
        """Invalidate refresh token only."""

        dec = decode_token(client_refresh_token, "refresh")
        decoded = dec.claims
        jti = decoded["jti"]
        user = decoded["sub"]

        db_token = await uow.tokens.get_refresh_token_by_jti(user_id=user, jti=jti)
        if not db_token:
            logger.warning(
                "Attempt to use revoked refresh token on logout: jti=%s", jti
            )
            raise TokenRevoked()

        try:
            verify_token(token=client_refresh_token, hashed_token=db_token.refresh_hash)
        except Exception as e:
            logger.warning(
                "Failed to verify refresh token on logout: jti=%s, reason=%s", jti, e
            )
            raise TokenInvalid() from e

        uow.tokens.delete_refresh_token(db_token)
