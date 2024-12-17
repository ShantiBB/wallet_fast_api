from typing import Annotated

from fastapi import Depends

from app.api.v1.routers.auth import fastapi_users
from app.user.models import User

current_user = fastapi_users.current_user(active=True)
CurrentUserDep = Annotated[User, Depends(current_user)]
