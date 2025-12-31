from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.label == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_default(self) -> Role:
        role = await self.get_by_name("user")
        if not role:
            raise ValueError("Default role not found")
        return role
