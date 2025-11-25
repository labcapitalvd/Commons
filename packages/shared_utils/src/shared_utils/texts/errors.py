class TextError(Exception):
    """Base error for TextUtils."""


class TextEmptyTarget(TextError):
    pass

class TextMaliciousTarget(TextError):
    pass

class TextMalformedTarget(TextError):
    pass
