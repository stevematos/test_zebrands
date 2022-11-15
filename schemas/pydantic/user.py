from pydantic import BaseModel

from config.constants import RolEnum


class UserSchema(BaseModel):
    email: str
    password: str | None = None
    full_name: str | None = None
    rol: RolEnum = None
