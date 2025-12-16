import os
import logging
from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared_models import User, Role
from shared_models.relationships import *


LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)

logger = logging.getLogger("api/db")
logger.setLevel(LOGLEVEL)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
 
    async def get_by_id(self, id: UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_username_or_email(
        self, username: Optional[str] = None, email: Optional[str] = None
    ) -> Optional[User]:
        if not username and not email:
            raise ValueError("Must provide username or email")
        stmt = select(User)
        if username:
            stmt = stmt.where(User.username == username)
        if email:
            stmt = stmt.where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user: User):
        self.session.add(user)
    
    async def add_role(self, user: User, role: Role):
        user.roles.append(role)  # SQLAlchemy handles the MN table

    async def remove_role(self, user: User, role: Role):
        user.roles.remove(role)


    async def delete(self, user: User):
        await self.session.delete(user)
