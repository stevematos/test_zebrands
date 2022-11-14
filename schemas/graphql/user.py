from enum import Enum
from typing import Optional

from strawberry import input, type, enum, union


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
    email: str
    password: Optional[str] = None
    full_name: Optional[str] = None
    rol: Optional[RolEnumInput] = None


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
class DeleteUserResponse:
    email: str
    message: str


@type
class UserError:
    message: str


CreateUserResult = union("CreateUserResult", (CreateUserResponse, UserError))
UpdateUserResult = union("UpdateUserResult", (UpdateUserResponse, UserError))
DeleteUserResult = union("DeleteUserResult", (DeleteUserResponse, UserError))
