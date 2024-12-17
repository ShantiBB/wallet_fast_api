from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase
)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID
)

from app.core.database.base import Base

if TYPE_CHECKING:
    from app.core.database.db_helper import AsyncSessionDep


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    @classmethod
    def get_db(cls, session: 'AsyncSessionDep'):
        return SQLAlchemyUserDatabase(session, cls)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):

    @classmethod
    async def get_access_token_db(cls, session: 'AsyncSessionDep'):
        yield SQLAlchemyAccessTokenDatabase(session, cls)
