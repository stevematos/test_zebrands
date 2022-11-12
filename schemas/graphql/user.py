from enum import Enum
from typing import Optional

from strawberry import input, type, enum, union, UNSET


@enum
class RolEnumInput(Enum):
    admin = "admin"
    anonymous = "anonymous"


@input
class CreateUserInput:
    email: str
    password: str
    full_name: str
    rol: RolEnumInput


@input
class UpdateUserInput:
    password: Optional[str] = UNSET
    full_name: Optional[str] = UNSET
    rol: Optional[RolEnumInput] = UNSET


@type
class CreateUserResponse:
    email: str
    full_name: str
    rol: RolEnumInput


@type
class UpdateUserResponse:
    full_name: str
    rol: RolEnumInput


@type
class UserError:
    message: str


CreateUserResult = union("CreateUserResult", (CreateUserResponse, UserError))
UpdateUserResult = union("UpdateUserResult", (UpdateUserResponse, UserError))
