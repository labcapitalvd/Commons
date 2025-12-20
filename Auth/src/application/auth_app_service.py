from domain import AuthService

class AuthAppService:
    def __init__(self, auth_service: AuthService, token_service: TokenService):
        self.auth_service = auth_service
        self.token_service = token_service

    async def login_and_issue_tokens(self, username: str, password: str):
        user = await self.auth_service.login(username, password)
        access_token = self.token_service.create_access(user)
        refresh_token = self.token_service.create_refresh(user)
        return access_token, refresh_token

    async def logout(self, user: User):
        await self.token_service.revoke_tokens(user)
