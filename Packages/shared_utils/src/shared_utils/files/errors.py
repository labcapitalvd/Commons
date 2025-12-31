class FileError(Exception):
    """Base error for FileDisk."""

class FileNameError(FileError):
    pass

class FileOSError(FileError):
    pass