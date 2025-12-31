from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import UserTier


class TierRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_label(self, label: str) -> Optional[UserTier]:
        stmt = select(UserTier).where(UserTier.label == label)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_default(self) -> UserTier:
        role = await self.get_by_label("STANDARD")
        if not role:
            raise ValueError("Default role not found")
        return role
