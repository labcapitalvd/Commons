import os
import logging
from typing import Optional
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid7

from joserfc import jwt, jws
from joserfc.jwk import OKPKey
from joserfc.errors import JoseError, InsecureClaimError

LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)
JWT_ASYMETRIC_ALGORITHM = os.environ["JWT_ASYMETRIC_ALGORITHM"]
JWT_EXPIRE_MINUTES_ACCESS = int(os.environ["JWT_EXPIRE_MINUTES_ACCESS"])
JWT_EXPIRE_MINUTES_REFRESH = int(os.environ["JWT_EXPIRE_MINUTES_REFRESH"])

JWT_PRIVATE_KEY_FILE = "/run/secrets/jwt_private_key"
if not os.path.exists(JWT_PRIVATE_KEY_FILE):
    raise FileNotFoundError(f"JWT_PRIVATE_KEY_FILE file not found at {JWT_PRIVATE_KEY_FILE}")
with open(JWT_PRIVATE_KEY_FILE, "rb") as f:
    JWT_PRIVATE_KEY = OKPKey.import_key(f.read())

logger = logging.getLogger("seed/users")
logger.setLevel(LOGLEVEL)

registry = jws.JWSRegistry(algorithms=[JWT_ASYMETRIC_ALGORITHM])


class TokenError(Exception):
    """Base error for TextUtils."""
    pass

class TokenTypeError(TokenError):
    """Wrong token type error."""
    pass

class TokenExpiredError(TokenError):
    """Token expired error.."""
    pass

class TokenEncodeError(TokenError):
    """Token encoding error."""
    pass


class TokenDecodeError(TokenError):
    """Token decoding error."""
    pass

class TokenIssuer:
    @staticmethod
    def generate_token(
        user_id: UUID, 
        username: str, 
        token_type: str = "access"
    ) -> tuple[str, int, Optional[str]]:
        """
        Generate either an access or refresh token.
        token_type: "access" | "refresh"
        """
        try:
            now = datetime.now(timezone.utc)

            expire_minutes = (
                JWT_EXPIRE_MINUTES_ACCESS
                if token_type == "access"
                else JWT_EXPIRE_MINUTES_REFRESH
            )
            exp = now + timedelta(minutes=expire_minutes)

            header = {"typ": "JWT", "alg": "EdDSA"}

            claims = {
                "sub": str(user_id),
                "username": username,
                "token_type": token_type,
                "iat": int(now.timestamp()),
                "exp": int(exp.timestamp()),
            }
            
            jti = None
            if token_type == "refresh":
                jti = str(uuid7())
                claims["jti"] = jti  # must be added BEFORE encoding
    
            token = jwt.encode(header, claims, JWT_PRIVATE_KEY, registry=registry)
            return token, int(exp.timestamp()), jti

        except InsecureClaimError:
            raise TokenEncodeError("Insecure claim error")

        except JoseError as e:
            logger.error(f"Error encoding {token_type} token: {e}")
            raise TokenEncodeError(f"Error encoding {token_type} token: {e}")
