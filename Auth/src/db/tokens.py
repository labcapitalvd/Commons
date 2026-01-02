from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import RefreshSession
from shared_utils.hashing import verify_token, hash_token
from shared_utils.tokens import decode_token


class TokenDb:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_refresh_token_entry(
        self,
        refresh_token: str,
    ) -> RefreshSession | None:
        """Fetch a User by ID, username, or email."""
        try:
            dec = decode_token(refresh_token, "refresh")
            decoded = dec.claims

            jti = decoded.get("jti")
            if not jti:
                raise ValueError("Missing JTI in token")

            stmt = select(RefreshSession).where(RefreshSession.jti == jti)
            result = await self.db.execute(stmt)
            session = result.scalar_one_or_none()

            if session and verify_token(refresh_token, session.refresh_hash):
                return session

            return None

        except Exception as e:
            raise

    async def create_refresh_token_entry(
        self, refresh_token: str
    ) -> RefreshSession | None:
        """Create a new refresh token entry."""
        try:
            dec = decode_token(refresh_token, "refresh")
            decoded = dec.claims

            jti = decoded["jti"]
            user_id = UUID(decoded["sub"])
            expires_at = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

            hashed_refresh = hash_token(refresh_token)

            session = RefreshSession(
                jti=jti,
                user_id=user_id,
                refresh_hash=hashed_refresh,
                expires_at=expires_at,
            )

            self.db.add(session)
            await self.db.commit()
            await self.db.refresh(session)
            return session

        except IntegrityError as e:
            await self.db.rollback()
            raise

        except Exception as e:
            await self.db.rollback()
            raise

    async def delete_refresh_token_entry(self, token: str) -> bool:
        """Create a new refresh token entry."""
        try:
            dec = decode_token(token, "refresh")
            decoded = dec.claims

            jti = decoded.get("jti")

            if not jti:
                raise ValueError("Missing JTI in token")

            result = await self.db.execute(
                select(RefreshSession).where(RefreshSession.jti == jti)
            )
            refresh_token = result.scalar_one_or_none()
            if not refresh_token:
                return False

            await self.db.delete(refresh_token)
            await self.db.commit()
            return True

        except IntegrityError as e:
            await self.db.rollback()
            raise

        except Exception as e:
            await self.db.rollback()
            raise
