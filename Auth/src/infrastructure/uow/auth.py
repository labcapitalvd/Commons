from shared_db import UnitOfWork

from ..repositories import UserRepository, RoleRepository, RefreshTokenRepository


class AuthUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        await super().__aenter__()
        assert self.session is not None

        self.users = UserRepository(self.session)
        self.roles = RoleRepository(self.session)
        self.tokens = RefreshTokenRepository(self.session)

        return self
