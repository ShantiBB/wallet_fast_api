import uuid

from fastapi_users import schemas


class CustomUser:
    username: str
    first_name: str
    last_name: str

class UserRead(schemas.BaseUser[uuid.UUID], CustomUser):
    pass


class UserCreate(schemas.BaseUserCreate, CustomUser):
    pass


class UserUpdate(schemas.BaseUserUpdate, CustomUser):
    pass
