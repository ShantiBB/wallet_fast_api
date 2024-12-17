from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase
)

from app.core.database.base import Base
from app.core.database.db_helper import AsyncSessionDep


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    @classmethod
    def get_user_db(cls, session: AsyncSessionDep):
        return SQLAlchemyUserDatabase(session, cls)
