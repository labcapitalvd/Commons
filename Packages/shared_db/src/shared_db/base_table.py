from uuid import UUID
from uuid-utils import uuid7
from enum import Enum
from typing import cast

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUIDType

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        UUIDType(as_uuid=True),
        primary_key=True,
        default=uuid7,
    )

class BaseTargetTable(Enum):
    def __init__(self, table_name: str, schema: str):
        self.table = table_name
        self.schema = schema

    @property
    def fq_name(self) -> str:
        return f"{self.schema}.{self.table}"

def merge_enums(name, *enums) -> type[BaseTargetTable]:
    members = {}
    for enum in enums:
        for item in enum:
            if item.name in members:
                raise ValueError(f"Duplicate enum member: {item.name}")
            members[item.name] = item.value

    MergedEnum = Enum(name, members, type=BaseTargetTable)

    # Cast to tell Pyright this is iterable over BaseTargetTable
    MergedEnumIter = cast(type[BaseTargetTable], MergedEnum)

    for member in MergedEnumIter:
        assert hasattr(member, "table") and hasattr(member, "schema"), f"{member.name} missing table/schema"

    return MergedEnumIter
