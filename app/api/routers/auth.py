import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from app.user.models import User
from app.authentication.backend import authentication_backend
from app.authentication.user_manager import UserManager
from app.user.schemas import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    UserManager.get_user_manager,
    [authentication_backend],
)


router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация'],
)

router.include_router(fastapi_users.get_auth_router(authentication_backend))
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
