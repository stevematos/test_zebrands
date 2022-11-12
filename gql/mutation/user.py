from strawberry.types import Info
from strawberry import (
    type,
    mutation,
)

from schemas.graphql.permission import (
    IsAuthenticated,
    IsAdmin,
)
from schemas.graphql.user import CreateUserInput, UpdateUserInput, CreateUserResult, UpdateUserResult, UserError
from schemas.pydantic.user import UserSchema
from services.user import add_user, updated_user
from utils.exceptions import UserDuplicated, UserNotFound


@type
class MutationUser:
    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def add_user(self, info: Info, user: CreateUserInput) -> CreateUserResult:
        try:
            return add_user(info.context['db'], UserSchema(
                email=user.email,
                password=user.password,
                full_name=user.full_name,
                rol=user.rol.value
            ))
        except UserDuplicated as e:
            return UserError(message=e)

    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def update_user(self, info: Info, user: UpdateUserInput) -> UpdateUserResult:
        try:
            return updated_user(info.context['db'], UserSchema(
                email=user.email,
                full_name=user.full_name,
                rol=user.rol.value
            ))
        except UserNotFound as e:
            return UserError(message=e)

