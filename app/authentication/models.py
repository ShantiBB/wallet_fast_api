from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID
)

from app.core.database.base import Base
from app.core.database.db_helper import AsyncSessionDep


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):

    @classmethod
    async def get_access_token_db(cls, session: AsyncSessionDep):
        yield SQLAlchemyAccessTokenDatabase(session, cls)
