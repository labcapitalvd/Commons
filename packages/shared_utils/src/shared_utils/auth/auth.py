import os
import logging
from uuid import UUID
from typing import Optional, Literal

from fastapi import Request, Response, Header, Body
from fastapi.security import OAuth2PasswordBearer

from shared_schemas import RefreshToken, ResponseWeb, ResponseMobile
from shared_utils.tokens import TokenChecker


VERSION = "0.1.0"
PRODUCTION_MODE = os.environ["PRODUCTION_MODE"].lower() in ("1", "true", "yes")
COOKIES_SECURE = False if not PRODUCTION_MODE else True
JWT_EXPIRE_MINUTES_REFRESH = int(os.environ["JWT_EXPIRE_MINUTES_REFRESH"])
LOGLEVEL = os.environ["LOGLEVEL"].lower() in (
    "debug",
    "info",
    "warning",
    "error",
    "critical",
)

COOKIES_SAMESITE: Literal["lax", "strict", "none"] = (
    "strict" if PRODUCTION_MODE and COOKIES_SECURE else "lax"
)

logger = logging.getLogger("api/main")
logger.setLevel(LOGLEVEL)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/public/api/login")


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
        self.token_checker = TokenChecker()

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
            logger.error("Failed to extract refresh token")
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
            dec = self.token_checker.decode_token(token, "access")
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
