import logging
from uuid import UUID
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.core.config import settings
from app.user.models import User

log = logging.getLogger(__name__)

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = (
        settings
        .access_token
        .reset_password_token_secret
    )
    verification_token_secret = (
        settings
        .access_token
        .verification_token_secret
    )

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ):
        log.warning('User %r has registered.', user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id, token
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning(
            'Verification requested for user %r. Verification token: %s',
            user.id, token
        )

    @classmethod
    async def get_user_manager(cls, user_db=Depends(User.get_user_db)):
        yield cls(user_db)
