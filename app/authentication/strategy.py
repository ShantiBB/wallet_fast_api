from typing import Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy
)

from .models import AccessToken
from app.core.config import settings

AccessTokenDep = Annotated[
    AccessTokenDatabase[AccessToken],
    Depends(AccessToken.get_access_token_db)
]


def get_database_strategy(
        access_token_db: AccessTokenDep
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds
    )
