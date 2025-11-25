import os
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_HOST = os.getenv("POSTGRES_HOST","db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","5432")
POSTGRES_PASSWORD_FILE = "/run/secrets/postgres_password"
if not os.path.exists(POSTGRES_PASSWORD_FILE):
    raise FileNotFoundError(f"POSTGRES_PASSWORD_FILE file not found at {POSTGRES_PASSWORD_FILE}")
with open(POSTGRES_PASSWORD_FILE, "r") as f:
    POSTGRES_PASSWORD = f.read().strip()

SYNC_DB = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
ASYNC_DB = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

sync_engine = create_engine(SYNC_DB)
async_engine = create_async_engine(ASYNC_DB)

SessionSync = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)
SessionAsync = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionAsync() as session:
        yield session
