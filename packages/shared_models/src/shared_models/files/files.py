from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from shared_models.targets import TargetTable

from shared_db import (
    Base,
    column_short_text,
    column_updated_at,
    column_fk,
    column_decimal,
)

if TYPE_CHECKING:
    from shared_models.auth.user_profiles import UserProfile
    from shared_models.links.link_user_file import UserFileLink
    from shared_models.reference.file_types import FileType

MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB


class File(Base):
    __tablename__ = TargetTable.FILES.table
    __table_args__ = {"schema": TargetTable.FILES.schema}

    user_id: Mapped[UUID] = column_fk(
        target=f"{TargetTable.USERS.fq_name}.id", ondelete="CASCADE"
    )
    file_type_id: Mapped[UUID] = column_fk(
        target=f"{TargetTable.FILE_TYPES.fq_name}.id", ondelete="CASCADE"
    )

    filename: Mapped[str] = column_short_text(length=64)
    filepath: Mapped[str] = column_short_text(length=255)
    filehash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    filesize: Mapped[Decimal] = column_decimal(precision=15, scale=0)

    
    updated_at: Mapped[datetime] = column_updated_at()

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="file", uselist=False
    )
    user_links: Mapped["UserFileLink"] = relationship(
        "UserFileLink", back_populates="file"
    )
    type: Mapped["FileType"] = relationship(
        "FileType", back_populates="file", uselist=False
    )
