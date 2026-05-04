"""Подключение к PostgreSQL — engine и session"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.config import settings

# движок для работы с БД
engine = create_async_engine(settings.db_url, echo=False)

# фабрика асинхронных сессий
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
