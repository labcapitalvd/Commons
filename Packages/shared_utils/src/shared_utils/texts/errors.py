class TextError(Exception):
    """Base error for TextUtils."""


class TextEmpty(TextError):
    """Text target is empty"""


class TextMalicious(TextError):
    """Text flagged as malicious"""


class TextMalformed(TextError):
    """Text flagged as malformed"""
