import os

from joserfc import jws
from joserfc.jwk import OKPKey

JWT_ASYMETRIC_ALGORITHM = os.environ["JWT_ASYMETRIC_ALGORITHM"]

JWT_EXPIRE_MINUTES_ACCESS = int(os.environ["JWT_EXPIRE_MINUTES_ACCESS"])
JWT_EXPIRE_MINUTES_REFRESH = int(os.environ["JWT_EXPIRE_MINUTES_REFRESH"])

JWT_PRIVATE_KEY_FILE = "/run/secrets/jwt_private_key"
JWT_PUBLIC_KEY_FILE = "/run/secrets/jwt_public_key"


def load_keys() -> tuple[OKPKey, OKPKey]:
    if not os.path.exists(JWT_PRIVATE_KEY_FILE):
        raise FileNotFoundError(
            f"JWT private key file not found at {JWT_PRIVATE_KEY_FILE}"
        )

    if not os.path.exists(JWT_PUBLIC_KEY_FILE):
        raise FileNotFoundError(
            f"JWT public key file not found at {JWT_PUBLIC_KEY_FILE}"
        )

    with open(JWT_PRIVATE_KEY_FILE, "rb") as f:
        private_key = OKPKey.import_key(f.read())

    with open(JWT_PUBLIC_KEY_FILE, "rb") as f:
        public_key = OKPKey.import_key(f.read())

    return private_key, public_key

PRIVATE_KEY, PUBLIC_KEY = load_keys()
REGISTRY = jws.JWSRegistry(algorithms=[JWT_ASYMETRIC_ALGORITHM])