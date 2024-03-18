from typing import AsyncGenerator

from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(settings.DB_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
