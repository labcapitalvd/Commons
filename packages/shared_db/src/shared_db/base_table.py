from uuid import UUID, uuid7
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUIDType

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )
