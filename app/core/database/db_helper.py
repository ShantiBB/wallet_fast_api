from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings


class DataBaseHelper:

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


db_helper = DataBaseHelper(
    url=settings.db_url,
    echo=settings.echo
)

SessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
