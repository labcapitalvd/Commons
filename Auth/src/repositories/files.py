from uuid import UUID
from datetime import datetime, timezone
from typing import Sequence, Optional
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError

from utils.allowed_types import FileTypeEnum

from shared_models import File, FileType


class FileRepository:
    """Repository for File and FileType aggregates. No commits/rollbacks here."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # --- FileType methods ---
    async def get_filetype(self, filetype_enum: FileTypeEnum) -> FileType:
        stmt = select(FileType).where(FileType.label == filetype_enum.label)
        result = await self.session.execute(stmt)
        return result.scalar_one()  # throws if not found

    # --- File queries ---
    async def get_file_by_id(self, id: UUID, owner: UUID) -> Optional[File]:
        stmt = select(File).where(File.id == id, File.user_id == owner)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_files(self, owner: UUID) -> Sequence[File]:
        stmt = select(File).where(File.user_id == owner)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_file_by_hash(self, owner: UUID, filehash: str) -> Optional[File]:
        stmt = select(File).where(File.user_id == owner, File.filehash == filehash)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # --- File modifications ---
    async def add_file(
        self,
        owner: UUID,
        file_type_id: UUID,
        filename: str,
        filepath: str,
        filehash: str,
        filesize: Decimal,
    ) -> File:
        new_file = File(
            user_id=owner,
            file_type_id=file_type_id,
            created_at=datetime.now(timezone.utc),
            filename=filename,
            filepath=filepath,
            filehash=filehash,
            filesize=filesize,
        )
        self.session.add(new_file)
        return new_file

    async def update_file(
        self,
        file: File,
        *,
        filetype_id: Optional[UUID] = None,
        filename: Optional[str] = None,
        filepath: Optional[str] = None,
        filehash: Optional[str] = None,
    ) -> File:
        if filetype_id is not None:
            file.file_type_id = filetype_id
        if filename is not None:
            file.filename = filename
        if filepath is not None:
            file.filepath = filepath
        if filehash is not None:
            file.filehash = filehash
        return file

    async def delete_file(self, file: File) -> None:
        await self.session.delete(file)
