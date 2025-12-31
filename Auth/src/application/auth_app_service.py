from domain import AuthService, TokenService
from infrastructure.uow import AuthUoW

from shared_models import User


class AuthAppService:
    def __init__(
        self,
        auth_service: AuthService | None = None,
        token_service: TokenService | None = None,
    ):
        self.auth_service = auth_service or AuthService()
        self.token_service = token_service or TokenService()

    async def register(self, username: str, email: str, password: str) -> User:
        async with AuthUoW() as uow:
            return await self.auth_service.register(
                username=username,
                email=email,
                password=password,
                uow=uow
            )

    async def login_and_issue_tokens(self, username: str, password: str) -> tuple[str,str]:
        async with AuthUoW() as uow:
            user = await self.auth_service.login(
                username=username,
                password=password,
                uow=uow
            )
            tokens = await self.token_service.issue_tokens(
                user_id=user.id,
                username=user.username,
                uow=uow
            )
            return tokens

    async def reauth_refresh(self, old_refresh_token: str) -> tuple[str,str]:
        async with AuthUoW() as uow:
            return await self.token_service.reauth(
                old_refresh_token=old_refresh_token,
                uow=uow
            )

    async def logout(self, refresh_token: str) -> None:
        async with AuthUoW() as uow:
            await self.token_service.logout(
                refresh_token=refresh_token,
                uow=uow
            )
