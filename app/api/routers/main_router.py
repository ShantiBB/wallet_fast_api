from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router
from .wallet import router as wallet_router

router = APIRouter(
    prefix='/api/v1',
)

router.include_router(router=auth_router)
router.include_router(router=user_router)

router.include_router(router=wallet_router)
