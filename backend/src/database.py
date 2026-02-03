from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import settings as main_config

engine = create_async_engine(
    main_config.DATABASE_URL,
    echo=main_config.SQL_ECHO,  # printing SQL Queries (good for debugging)
    pool_size=main_config.POOL_SIZE,  # connection pool size
    max_overflow=main_config.MAX_OVERFLOW,  # max extra connections
)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    # objects stay fresh after commit (if false selected), e.g. if you save user and would want to access its fields afterward
    # it will result in error or extra query, but with false selected you just access the fields
    expire_on_commit=main_config.EXPIRE_ON_COMMIT
)
# basically the class from which all my models will inherit from, in simple terms Base set up the mapping between
# db and my python classes
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            # yield is used here to kinda pause the function and then resume from the place it stopped
            # useful for closing the connection for db after route handler executes even if fails
            yield session
        finally:
            await session.close()


DB_Session = Annotated[AsyncSession, Depends(get_db)]
