from sqlalchemy.orm import Mapped, relationship

from shared_db import Base, column_long_text,column_short_text

from ..targets import TargetTable
from .. import ActivityLog

class LogActionType(Base):
    __tablename__ = TargetTable.LOG_ACTION_TYPES.table
    __table_args__ = {"schema": TargetTable.LOG_ACTION_TYPES.schema}

    label: Mapped[str] = column_short_text(length=255)
    description: Mapped[str] = column_long_text()

    log: Mapped["ActivityLog"] = relationship(
        "ActivityLog", back_populates="type", uselist=False
    )
