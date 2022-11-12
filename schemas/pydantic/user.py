from typing import Optional

from pydantic import BaseModel

from config.constants import RolEnum


class UserSchema(BaseModel):
    email:  Optional[str] = None
    password: Optional[str] = None
    full_name: str
    rol: RolEnum
