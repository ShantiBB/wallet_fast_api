from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings


class SyncDataBase:

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_engine(
            url=url,
            echo=echo
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    async def get_session(self):
        with self.session_factory() as session:
            yield session


class AsyncDataBase:

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


sync_database = SyncDataBase(
    url=settings.postgres.sync_url,
    echo=settings.postgres.echo
)
async_database = AsyncDataBase(
    url=settings.postgres.async_url,
    echo=settings.postgres.echo
)

SyncSessionDep = Annotated[Session, Depends(sync_database.get_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(async_database.get_session)]
