from domain import AuthService, TokenService
from infrastructure.uow import AuthUoW


class AuthAppService:
    def __init__(self, auth_service: AuthService, token_service: TokenService):
        self.auth_service = auth_service
        self.token_service = token_service

    async def login_and_issue_tokens(self, username: str, password: str):
        async with AuthUoW() as uow:
            user = await self.auth_service.login(
                username=username, password=password, uow=uow
            )
            tokens = await self.token_service.issue_tokens(
                user.id, user.username, uow=uow
            )
            return tokens

    async def reauth_refresh(self, old_refresh_token: str):
        async with AuthUoW() as uow:
            return await self.token_service.reauth(
                old_refresh_token=old_refresh_token, uow=uow
            )

    async def logout(self, refresh_token: str):
        async with AuthUoW() as uow:
            await self.token_service.logout(
                refresh_token=refresh_token, uow=uow
            )
