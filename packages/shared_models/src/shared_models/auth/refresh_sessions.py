from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship

from shared_models.targets import TargetTable

from shared_db import (
    Base,
    column_short_text,
    column_bool,
    column_fk,
    column_datetime,
    column_uuid
)

if TYPE_CHECKING:
    from shared_models.auth.users import User


class RefreshSession(Base):
    __tablename__ = TargetTable.REFRESH_SESSIONS.table
    __table_args__ = {"schema": TargetTable.REFRESH_SESSIONS.schema}

    user_id: Mapped[UUID] = column_fk(target=f"{TargetTable.USERS.fq_name}.id")

    jti: Mapped[UUID] = column_uuid()
    refresh_hash: Mapped[str] = column_short_text()

    
    expires_at: Mapped[datetime] = column_datetime()
    revoked: Mapped[bool] = column_bool()

    user: Mapped["User"] = relationship("User", back_populates="refresh_sessions")
