from typing import TYPE_CHECKING
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

if TYPE_CHECKING:
    from shared_models.reference.user_tiers import UserTier
    from shared_models.auth.user_profiles import UserProfile
    from shared_models.auth.user_details import UserDetails
    from shared_models.interactions.notifications import Notification
    from shared_models.interactions.comments import Comment
    from shared_models.links.link_user_actor import UserActorLink
    from shared_models.links.link_user_submission import UserSubmissionLink
    from shared_models.links.link_user_file import UserFileLink
    from shared_models.auth.refresh_sessions import RefreshSession


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

    actor_links: Mapped["UserActorLink"] = relationship(
        "UserActorLink", back_populates="user"
    )
    submission_links: Mapped["UserSubmissionLink"] = relationship(
        "UserSubmissionLink", back_populates="user"
    )
    file_links: Mapped["UserFileLink"] = relationship(
        "UserFileLink", back_populates="user"
    )
    refresh_sessions: Mapped["RefreshSession"] = relationship(
        "RefreshSession", back_populates="user"
    )
