class HashError(Exception):
    """Base error for HashUtils."""


class EmptyHashTarget(HashError):
    pass
