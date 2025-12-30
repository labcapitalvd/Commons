from typing import Optional
from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from shared_utils import get_logger
from shared_models import RefreshSession


logger = get_logger("api/db")


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_refresh_token_by_jti(self, jti: str) -> Optional[RefreshSession]:
        stmt = select(RefreshSession).where(RefreshSession.jti == jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def create_refresh_token(self, token: RefreshSession) -> None:
        session = cast(Session, self.session)
        session.add(token)

    def delete_refresh_token(self, token: RefreshSession) -> None:
        session = cast(Session, self.session)
        session.delete(token)
