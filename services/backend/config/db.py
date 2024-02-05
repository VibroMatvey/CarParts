from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config.const import env

SQLALCHEMY_DATABASE_URL = env['DB_URL']

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
