import os
import shutil

from fastapi import UploadFile

import aiofiles

from .errors import FileError, FileNameError, FileOSError


class FileDisk:
    async def save_file(
        self,
        file: UploadFile,
        filename: str,
        filepath: str,
    ) -> bool:
        """Save the file to disk"""

        if not filename:
            raise FileNameError("Filename cannot be empty.")

        os.makedirs(filepath, exist_ok=True)

        file_path = os.path.join(filepath, filename)

        try:
            temp_path = f"{file_path}.part"
            async with aiofiles.open(temp_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):
                    await f.write(chunk)
            await f.flush()
            os.rename(temp_path, file_path)
            return True
        except OSError as e:
            raise FileOSError(f"Filesystem error {e}")
        except Exception as e:
            raise FileError(f"Unexpected error while saving: {e}")

    async def rename_file(
        self,
        old_filename: str,
        new_filename: str,
        filepath: str,
    ) -> bool:
        """Overwrite the file to disk"""

        if not new_filename:
            raise FileNameError("Filename must not be empty.")

        old_file_path = os.path.join(filepath, old_filename)
        new_file_path = os.path.join(filepath, new_filename)

        try:
            shutil.move(old_file_path, new_file_path)
            return True
        except OSError as e:
            raise FileOSError(f"Filesystem error {e}")
        except Exception as e:
            raise FileError(f"Unexpected error occurred while renaming: {e}")

    async def delete_file(
        self,
        filename: str,
        filepath: str,
    ) -> bool:
        """Save the file to disk"""

        if not filename:
            raise FileNameError("Filename must not be empty.")
        file_path = os.path.join(filepath, filename)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                raise FileError("File not found.")
        except OSError as e:
            raise FileOSError(f"Filesystem error: {e}")
        except Exception as e:
            raise FileError(f"Unexpected error while deleting file: {e}")
