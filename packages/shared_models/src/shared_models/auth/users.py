from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship

from shared_models.targets import TargetTable

from shared_db import (
    Base,
    column_decimal,
    column_short_text,
    column_updated_at,
    column_bool,
    column_fk,
)


class User(Base):
    __tablename__ = TargetTable.USERS.table
    __table_args__ = {"schema": TargetTable.USERS.schema}

    tier_id: Mapped[UUID] = column_fk(target=f"{TargetTable.USER_TIERS.fq_name}.id")

    username: Mapped[str] = column_short_text(length=32, unique=True)
    email: Mapped[str] = column_short_text(length=100, unique=True)
    password_hash: Mapped[str] = column_short_text()
    is_active: Mapped[bool] = column_bool(default=False)
    is_verified: Mapped[bool] = column_bool(default=False)

    
    updated_at: Mapped[datetime] = column_updated_at()

    media_usage: Mapped[Decimal] = column_decimal(
        precision=15, scale=0, default=Decimal(0)
    )

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="user", uselist=False
    )
    details: Mapped["UserDetails"] = relationship(
        "UserDetails", back_populates="user", uselist=False
    )
    tier: Mapped["UserTier"] = relationship(
        "UserTier", back_populates="user", uselist=False
    )
    notifications: Mapped["Notification"] = relationship(
        "Notification", back_populates="user"
    )
    comments: Mapped["Comment"] = relationship("Comment", back_populates="user")

    file_links: Mapped["UserFileLink"] = relationship(
        "UserFileLink", back_populates="user"
    )
    refresh_sessions: Mapped["RefreshSession"] = relationship(
        "RefreshSession", back_populates="user"
    )
