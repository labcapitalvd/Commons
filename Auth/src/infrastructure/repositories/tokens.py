from typing import cast

from shared_models import RefreshSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_refresh_token_by_jti(self, jti: str) -> RefreshSession | None:
        stmt = select(RefreshSession).where(RefreshSession.jti == jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def create_refresh_token(self, token: RefreshSession) -> None:
        session = cast(Session, self.session)
        session.add(token)

    def delete_refresh_token(self, token: RefreshSession) -> None:
        session = cast(Session, self.session)
        session.delete(token)
