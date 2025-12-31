from shared_db import UnitOfWork

from ..repositories import UserRepository, RoleRepository, RefreshTokenRepository


class AuthUoW(UnitOfWork):
    async def __aenter__(self):
        await super().__aenter__()
        assert self.session is not None

        self.users: UserRepository = UserRepository(self.session)
        self.roles: RoleRepository = RoleRepository(self.session)
        self.tokens: RefreshTokenRepository = RefreshTokenRepository(self.session)

        return self
