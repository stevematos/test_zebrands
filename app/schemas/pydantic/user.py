from config.constants import RolEnum
from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    password: str | None = None
    full_name: str | None = None
    rol: RolEnum = None
