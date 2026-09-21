from typing import AsyncGenerator, Any, Generator
from sqlalchemy.ext.asyncio import(
  create_async_engine,
  AsyncSession,
  async_sessionmaker,
)
from sqlalchemy.testing import future
from sqlmodel import SQLModel

DATABASE_URL="sqlite+aiosqlite:///./orm/books.db"

# 创建异步引擎
engine =create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# 创建异步异步session工厂
async_session=async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 初始化数据库
async def init_db()->None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
async def get_session() -> Generator[AsyncSession, None]:
    async with async_session() as session:
        yield  session