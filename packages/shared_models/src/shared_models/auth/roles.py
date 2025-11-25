from sqlalchemy.orm import Mapped, relationship

from shared_db import Base, column_long_text, column_short_text

from shared_models.targets import TargetTable


class Role(Base):
    __tablename__ = TargetTable.ROLES.table
    __table_args__ = {"schema": TargetTable.ROLES.schema}

    label: Mapped[str] = column_short_text(length=255)
    description: Mapped[str] = column_long_text()

    user_actor_link: Mapped["UserActorLink"] = relationship(
        "UserActorLink", back_populates="roles"
    )
    user_submission_link: Mapped["UserSubmissionLink"] = relationship(
        "UserSubmissionLink", back_populates="roles"
    )
    user_file_link: Mapped["UserFileLink"] = relationship(
        "UserFileLink", back_populates="roles"
    )
