from enum import Enum
from typing import Optional

from strawberry import input, type, enum, union


@enum
class RolEnumInput(Enum):
    admin = "admin"
    anonymous = "anonymous"


@input
class UserInput:
    email: str
    password: str
    full_name: str
    rol: RolEnumInput


class CreateUserInput(UserInput):
    pass


class UpdateUserInput(UserInput):
    password: Optional[str] = None
    full_name: Optional[str] = None
    rol: Optional[RolEnumInput] = None


@type
class UserResponse:
    email: str
    full_name: str
    rol: RolEnumInput


@type
class CreateUserResponse(UserResponse):
    pass


@type
class UpdateUserResponse(UserResponse):
    pass


@type
class DeleteUserResponse(UserResponse):
    message: str


@type
class UserError:
    message: str


CreateUserResult = union("CreateUserResult", (CreateUserResponse, UserError))
UpdateUserResult = union("UpdateUserResult", (UpdateUserResponse, UserError))
DeleteUserResult = union("DeleteUserResult", (DeleteUserResponse, UserError))
