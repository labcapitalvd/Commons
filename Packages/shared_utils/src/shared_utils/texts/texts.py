import re
import hashlib
import unicodedata

from .errors import TextEmptyTarget, TextMalformedTarget


MAX_TEXT_LENGTH = 10_000
MAX_EMAIL_LENGTH = 254

CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
MULTISPACE_RE = re.compile(r"[ ]{2,}")
EMOJI_RE = re.compile(
    "["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "]+",
    flags=re.UNICODE,
)
HTML_TAG_RE = re.compile(r"<[^>]+>")
EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)


def normalize_text(text: str) -> str:
    if not text or not text.strip():
        raise TextEmptyTarget("Text is empty.")

    return unicodedata.normalize("NFKC", text)


def sanitize_text(
    text: str,
    *,
    remove_emojis: bool = False,
    remove_html: bool = False,
) -> str:
    if not text or not text.strip():
        raise TextEmptyTarget("Sanitation target is empty.")

    if len(text) > MAX_TEXT_LENGTH:
        raise TextMalformedTarget("Text too long.")

    text = CONTROL_CHARS_RE.sub("", text)

    if remove_html:
        text = HTML_TAG_RE.sub("", text)

    if remove_emojis:
        text = EMOJI_RE.sub("", text)

    text = MULTISPACE_RE.sub(" ", text)

    if not text.strip():
        raise TextEmptyTarget("Sanitation removed all content.")

    return text


def validate_email(email: str) -> str:
    if not email or not email.strip():
        raise TextEmptyTarget("Email is empty.")

    email = unicodedata.normalize("NFKC", email).strip()

    if len(email) > MAX_EMAIL_LENGTH:
        raise TextMalformedTarget("Email too long.")

    if not EMAIL_RE.fullmatch(email):
        raise TextMalformedTarget("Invalid email format.")

    return email


def hash_text(text: str) -> str:
    if not text or not text.strip():
        raise TextEmptyTarget("Text to hash is empty.")

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
