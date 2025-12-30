from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["argon2"],
    argon2__time_cost=3,
    argon2__memory_cost=131072,  # 128 MB
    argon2__parallelism=2,
)

token_context = CryptContext(
    schemes=["argon2"],
    argon2__time_cost=1,
    argon2__memory_cost=65536,   # 64 MB
    argon2__parallelism=1,
)

fast_context = CryptContext(
    schemes=["argon2"],
    argon2__time_cost=1,
    argon2__memory_cost=16384,   # 16 MB
    argon2__parallelism=1,
)