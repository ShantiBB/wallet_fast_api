from fastapi import APIRouter

from app.api.routers.auth import fastapi_users
from app.user.schemas import UserRead, UserUpdate

router = APIRouter(
    prefix='/users',
    tags=['Пользователи'],
)
router.include_router(
    fastapi_users.get_users_router(
        UserRead,
        UserUpdate
    )
)
