from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, relationship

from shared_models.targets import TargetTable

from shared_db import Base, column_fk, column_updated_at


class UserFileLink(Base):
    __tablename__ = TargetTable.LINK_USER_FILE.table
    __table_args__ = {"schema": TargetTable.LINK_USER_FILE.schema}

    user_id: Mapped[UUID] = column_fk(
        target=f"{TargetTable.USERS.fq_name}.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    file_id: Mapped[UUID] = column_fk(
        target=f"{TargetTable.FILES.fq_name}.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    role_id: Mapped[UUID] = column_fk(
        target=f"{TargetTable.ROLES.fq_name}.id",
        primary_key=True,
        ondelete="SET NULL",
    )

    
    updated_at: Mapped[datetime] = column_updated_at()

    user: Mapped["User"] = relationship("User", back_populates="file_links")
    file: Mapped["File"] = relationship("File", back_populates="user_links")
    roles: Mapped["Role"] = relationship("Role", back_populates="user_file_link")
