from typing import Optional
from pydantic import BaseModel
from config.constants import RolEnum


class UserSchema(BaseModel):
    email:  str
    password: Optional[str] = None
    full_name: Optional[str] = None
    rol: RolEnum = None
