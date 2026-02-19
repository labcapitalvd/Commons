import os

from shared_utils.logger import get_logger

logger = get_logger(__name__)

FERNET_KEY_FILE = "/run/secrets/fernet_key"


def load_fernet_key() -> bytes:
    if not os.path.exists(FERNET_KEY_FILE):
        logger.critical("Fernet key missing at %s", FERNET_KEY_FILE)
        raise RuntimeError("Fernet key not configured. Mount /run/secrets/fernet_key")

    with open(FERNET_KEY_FILE, "rb") as f:
        key = f.read().strip()
        if len(key) != 44:
            logger.critical("Invalid Fernet key length (%d)", len(key))
            raise RuntimeError("Invalid Fernet key")
        return key


env_key = os.environ.get("FERNET_KEY")

if env_key:
    # Ensure it's converted to bytes if it comes from the environment
    FERNET_KEY: bytes = env_key.encode() if isinstance(env_key, str) else env_key
else:
    FERNET_KEY: bytes = load_fernet_key()
