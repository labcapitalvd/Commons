import logging
import os
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import RefreshSession

LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)

logger = logging.getLogger("api/db")
logger.setLevel(LOGLEVEL)


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_jti(self, jti: str) -> Optional[RefreshSession]:
        stmt = select(RefreshSession).where(RefreshSession.jti == jti)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, session: RefreshSession) -> None:
        self.session.add(session)

    async def delete(self, session: RefreshSession) -> None:
        await self.session.delete(session)
