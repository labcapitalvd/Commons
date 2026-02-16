import os
from datetime import datetime, timedelta, timezone
from typing import Literal, Annotated
from uuid import UUID
from uuid_utils import uuid7

from fastapi import Request, Response, Header, HTTPException, Cookie, Body, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from joserfc import jwt
from joserfc.errors import (
    BadSignatureError,
    ConflictAlgorithmError,
    DecodeError,
    ExceededSizeError,
    ExpiredTokenError,
    InsecureClaimError,
    InvalidExchangeKeyError,
    JoseError,
)

from shared_schemas import RefreshToken

from .config import (
    JWT_EXPIRE_MINUTES_ACCESS,
    JWT_EXPIRE_MINUTES_REFRESH,
    PRIVATE_KEY,
    PUBLIC_KEY,
    REGISTRY,
)

from .errors import (
    TokenEncodeError,
    TokenDecodeError,
    TokenTypeError,
    TokenSignatureError,
    TokenExpiredError,
    TokenEmptyError,
    InvalidPlatformError,
)


PRODUCTION_MODE = os.getenv("PRODUCTION_MODE", "false").lower() in ("1", "true", "yes")

COOKIES_SECURE = False if not PRODUCTION_MODE else True
COOKIES_SAMESITE = "strict" if PRODUCTION_MODE and COOKIES_SECURE else "lax"

security = HTTPBearer(auto_error=False)

TokenType = Literal["access", "refresh"]


def generate_token(
    user_id: UUID, username: str, token_type: TokenType = "access"
) -> tuple[str, int, str | None]:
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
            claims["jti"] = jti

        token = jwt.encode(header, claims, PRIVATE_KEY, registry=REGISTRY)
        return token, int(exp.timestamp()), jti

    except InsecureClaimError as e:
        raise TokenEncodeError("Insecure claim error") from e

    except JoseError as e:
        raise TokenEncodeError(f"Error encoding {token_type} token") from e


def decode_token(token: str, expected_type: TokenType):
    """
    Decode a JWT and validate its type.
    expected_type: "access" | "refresh"
    """
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["EdDSA"],
        )

        if payload.claims.get("token_type") != expected_type:
            raise TokenTypeError(f"Token must be a {expected_type} token")

        return payload

    except BadSignatureError:
        raise TokenSignatureError("Invalid token signature")

    except ConflictAlgorithmError:
        raise TokenDecodeError("Invalid token algorithm")

    except DecodeError:
        raise TokenDecodeError("Invalid token")

    except ExpiredTokenError:
        raise TokenExpiredError(f"{expected_type.capitalize()} token expired")

    except ExceededSizeError:
        raise TokenDecodeError("Token exceeded size limit")

    except InvalidExchangeKeyError:
        raise TokenDecodeError("Invalid exchange key")

    except JoseError as e:
        raise TokenDecodeError(f"Error decoding {expected_type} token") from e


class TokenContext:
    def __init__(
        self,
        response: Response,
        platform: Annotated[str, Header(alias="X-Platform")] = "web",
    ):
        self.response = response
        self.platform = platform

    def set_refresh_cookie(self, refresh_token: str):
        if self.platform == "web":
            self.response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=COOKIES_SECURE,
                samesite=COOKIES_SAMESITE,
                max_age=(JWT_EXPIRE_MINUTES_REFRESH * 60) - 120,
                path="/auth/reauth",
            )

    def unset_refresh_cookie(self):
        if self.platform == "web":
            self.response.delete_cookie(
                key="refresh_token",
                httponly=True,
                secure=COOKIES_SECURE,
                samesite=COOKIES_SAMESITE,
            )

async def get_refresh_token(
    request: Request,
    platform: Annotated[str, Header(alias="X-Platform")] = "web",
    cookie_token: Annotated[str | None, Cookie(alias="refresh_token")] = None,
    bearer_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(security)
    ] = None,
) -> str:
    """
    Smart dependency that looks for the token in the right place
    based on the X-Platform header.
    Web -> Cookie
    Mobile -> Authorization: Bearer <token>
    """
    if platform == "web":
        if not cookie_token:
            raise TokenEmptyError("Missing refresh token in cookies")
        return cookie_token

    elif platform == "mobile":
        if not bearer_token or not bearer_token.credentials:
            raise TokenEmptyError("Missing refresh token in Authorization header")
        return bearer_token.credentials

    raise InvalidPlatformError(f"Unknown platform: {platform}")
