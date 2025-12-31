
from uuid import UUID
from datetime import datetime, timezone

from shared_utils import HashUtils
from shared_models import RefreshSession
from shared_utils import TokenIssuer, TokenVerifier

from infrastructure.uow import AuthUoW

from .errors import TokenRevoked, TokenInvalid


class TokenCrypto:
    @staticmethod
    def hash_refresh_token(raw: str) -> str:
        try:
            return HashUtils.hash_token(raw)
        except Exception as e:
            raise RuntimeError("Failed to hash refresh token") from e

    @staticmethod
    def verify_refresh_token(raw: str, hashed: str) -> bool:
        try:
            return HashUtils.verify_token(raw, hashed)
        except Exception:
            return False


class TokenService:
    async def issue_tokens(
        self,
        user_id: UUID, 
        username: str, 
        uow: AuthUoW
    ) -> tuple[str, str]:
        """Generate access and refresh tokens"""
        access_token, _, _ = TokenIssuer.generate_token(user_id, username, "access")
        refresh_token, expr, jti = TokenIssuer.generate_token(user_id, username, "refresh")
        
        if jti is None:
            raise ValueError("Refresh token must have a jti")
            
        refresh_hash = TokenCrypto.hash_refresh_token(refresh_token)
        
        db_token = RefreshSession(
            jti=jti,
            user_id=user_id,
            refresh_hash=refresh_hash,
            expires_at=datetime.fromtimestamp(expr, tz=timezone.utc),
        )

        
        uow.tokens.create_refresh_token(db_token)
        return access_token, refresh_token


    async def reauth(
        self,
        old_refresh_token: str,
        uow: AuthUoW
    ) -> tuple[str, str]:
        """Invalidate old refresh token and issue new tokens."""
            
        dec = TokenVerifier.decode_token(old_refresh_token, "refresh")
        decoded = dec.claims
        jti = decoded["jti"]
        
        old_token = await uow.tokens.get_refresh_token_by_jti(jti)
        if not old_token:
            raise TokenRevoked()
        
        if not TokenCrypto.verify_refresh_token(
            old_refresh_token,
            old_token.refresh_hash
        ):
            raise TokenInvalid()

        
        uow.tokens.delete_refresh_token(old_token)
        
        return await self.issue_tokens(
            UUID(decoded["sub"]),
            decoded["username"],
            uow=uow
        )


    async def logout(
        self,
        refresh_token: str,
        uow: AuthUoW
    ) -> None:
        """Invalidate refresh token only."""

        dec = TokenVerifier.decode_token(refresh_token, "refresh")
        decoded = dec.claims
        
        jti = decoded["jti"]
        
        old_token = await uow.tokens.get_refresh_token_by_jti(jti)
        if not old_token:
            raise TokenRevoked()
        
        if not TokenCrypto.verify_refresh_token(
            refresh_token,
            old_token.refresh_hash
        ):
            raise TokenInvalid()

        
        uow.tokens.delete_refresh_token(old_token)
