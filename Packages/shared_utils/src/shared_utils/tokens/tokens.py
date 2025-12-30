import os
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional
from uuid import UUID, uuid7

from fastapi.security import OAuth2PasswordBearer
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

from .config import (
    JWT_ASYMETRIC_ALGORITHM,
    JWT_EXPIRE_MINUTES_ACCESS,
    JWT_EXPIRE_MINUTES_REFRESH,
    PRIVATE_KEY,
    PUBLIC_KEY,
    REGISTRY,
)
from .errors import (
    TokenDecodeError,
    TokenEncodeError,
    TokenExpiredError,
    TokenTypeError,
)

from shared_utils import get_logger


PRODUCTION_MODE = os.environ["PRODUCTION_MODE"].lower() in ("1", "true", "yes")
COOKIES_SECURE = False if not PRODUCTION_MODE else True


COOKIES_SAMESITE: Literal["lax", "strict", "none"] = (
    "strict" if PRODUCTION_MODE and COOKIES_SECURE else "lax"
)

logger = get_logger("shared_utils/tokens")

TokenType = Literal["access", "refresh"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/public/api/login")


class TokenIssuer:
    @staticmethod
    def generate_token(
        user_id: UUID, username: str, token_type: TokenType = "access"
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

            token = jwt.encode(header, claims, PRIVATE_KEY, registry=REGISTRY)
            return token, int(exp.timestamp()), jti

        except InsecureClaimError:
            raise TokenEncodeError("Insecure claim error")

        except JoseError as e:
            logger.error(f"Error encoding {token_type} token: {e}")
            raise TokenEncodeError(f"Error encoding {token_type} token: {e}")


class TokenVerifier:
    @staticmethod
    def decode_token(token: str, expected_type: TokenType):
        """
        Decode a JWT and validate its type.
        expected_type: "access" | "refresh"
        """
        try:
            payload = jwt.decode(
                token, PUBLIC_KEY, algorithms=[JWT_ASYMETRIC_ALGORITHM]
            )
            if payload.claims.get("token_type") != expected_type:
                raise TokenTypeError(f"Token must be a {expected_type} token")
            return payload

        except BadSignatureError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid signature"
            )

        except ConflictAlgorithmError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid algorithm"
            )

        except DecodeError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid token"
            )

        except ExpiredTokenError:
            raise TokenExpiredError(f"{expected_type.capitalize()} token expired")

        except ExceededSizeError:
            raise TokenDecodeError(
                f"{expected_type.capitalize()} token exceeded size limit"
            )

        except InvalidExchangeKeyError:
            raise TokenDecodeError(
                f"Error decoding {expected_type} token: Invalid exchange key"
            )

        except JoseError as e:
            raise TokenDecodeError(f"Error decoding {expected_type} token: {str(e)}")


class TokenContext:
    def __init__(
        self,
        request: Request,
        response: Response,
        platform: str = Header(default="web", alias="X-Platform"),
    ):
        self.request = request
        self.response = response
        self.platform = platform

    async def extract_access(self) -> str:
        """Extract token from header"""
        token = self.request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            logger.error("Invalid token")
            raise
        return token.split(" ", 1)[1]

    async def extract_refresh(
        self, body: Optional[RefreshToken] = Body(default=None)
    ) -> str:
        """Extract token from cookie, or JSON body."""
        try:
            if self.platform == "web":
                token = self.request.cookies.get("refresh_token")
                if not token:
                    logger.error("Invalid refresh token")
                    raise
                return token

            elif self.platform == "mobile":
                if body is None:
                    logger.error("Invalid refresh token")
                    raise
                token = body.refresh_token
                return token

            else:
                logger.error("Invalid platform")
                raise

        except Exception as e:
            logger.error(f"Failed to extract refresh token -> {e}")
            raise

    def set_refresh_cookie(self, refresh_token: str):
        """For web: attach secure cookie."""
        if self.platform == "web":
            self.response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=COOKIES_SECURE,
                samesite=COOKIES_SAMESITE,
                max_age=(JWT_EXPIRE_MINUTES_REFRESH * 60) - 120,
                path="/",
            )

    def make_return(self, access_token: str, refresh_token: str):
        """Unified return logic."""
        if self.platform == "web":
            self.set_refresh_cookie(refresh_token)
            return ResponseWeb(access_token=access_token)
        elif self.platform == "mobile":
            return ResponseMobile(
                access_token=access_token, refresh_token=refresh_token
            )
        logger.error("Invalid platform")
        raise

    async def get_current_user(self) -> UUID:
        """Decode access token and return user object."""
        token = await self.extract_access()
        try:
            dec = self.decode_token(token, "access")
            payload = dec.claims
            user_id = UUID(payload["sub"])
            return user_id
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            raise


async def get_refresh_token(
    request: Request,
    platform: str = Header(default="web", alias="X-Platform"),
    body: Optional[RefreshToken] = Body(None),
) -> str:
    ctx = TokenContext(request=request, response=Response(), platform=platform)
    return await ctx.extract_refresh(body)
