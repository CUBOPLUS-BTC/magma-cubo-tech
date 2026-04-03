from sqlmodel import SQLModel, create_engine, Session, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
