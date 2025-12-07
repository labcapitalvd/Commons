from sqlalchemy.orm import Mapped, relationship

from shared_db import Base, column_long_text, column_short_text

from ..targets import TargetTable
from .. import Comment


class CommentType(Base):
    __tablename__ = TargetTable.COMMENT_TYPES.table
    __table_args__ = {"schema": TargetTable.COMMENT_TYPES.schema}

    label: Mapped[str] = column_short_text(length=255)
    description: Mapped[str] = column_long_text()

    comment: Mapped["Comment"] = relationship(
        "Comment", back_populates="type", uselist=False
    )
