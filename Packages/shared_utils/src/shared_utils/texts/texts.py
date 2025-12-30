import html
import re
import hashlib
import unicodedata

from shared_utils.texts.errors import TextError, TextEmptyTarget, TextMaliciousTarget, TextMalformedTarget


class TextUtils:
    @staticmethod
    def sanitize_text(
        text: str, 
        remove_emojis: bool = False, 
        remove_html: bool = False
    ) -> str:
        if not text or text.strip() == "":
            raise TextEmptyTarget("Sanitation target is empty.")

        text = unicodedata.normalize("NFKC", text)
        text = re.sub(
            r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text
        )  # Remove control characters except \t, \n, \r

        if remove_html:
            text = re.sub(r"<[^>]+>", "", text)

        if remove_emojis:
            emoji_pattern = re.compile(
                "["
                "\U0001f600-\U0001f64f"  # emoticons
                "\U0001f300-\U0001f5ff"  # symbols & pictographs
                "\U0001f680-\U0001f6ff"  # transport & map symbols
                "\U0001f1e0-\U0001f1ff"  # flags
                "]+",
                flags=re.UNICODE,
            )
            text = emoji_pattern.sub(r"", text)

        # Collapse multiple spaces but preserve line breaks
        text = re.sub(r"[ ]{2,}", " ", text)

        if not text.strip():
            raise TextEmptyTarget("Sanitation target is empty.")

        return text

    @staticmethod
    def is_valid_and_safe_email(
        email: str
    ) -> str:
        # Trim whitespace and escape basic HTML actors
        text = email.strip()
        text = html.escape(text)

        # Reject malicious patterns
        if any(
            bad in text.lower()
            for bad in ["<script", "javascript:", ";", "|", "`", "$(", "base64"]
        ):
            raise TextMaliciousTarget("Email is malicious.")

        # Email regex (simplified but effective)
        email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        if not email_regex.match(text):
            raise TextMalformedTarget("Invalid email.")

        return text

    @staticmethod
    def generate_text_hash(
        text: str
    ) -> str:
        """Generate SHA-256 hash of a given string."""
        try:
            if not text or text.strip() == "":
                raise TextEmptyTarget("Text to hash is empty.")
            return hashlib.sha256(text.encode("utf-8")).hexdigest()
        except Exception as e:
            raise TextError(f"Exception occurred while generating hash: {e}")
