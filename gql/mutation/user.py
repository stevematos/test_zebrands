from strawberry import mutation, type
from strawberry.types import Info

from config.exceptions import UserDuplicated, UserNotFound
from schemas.graphql.permission import IsAdmin, IsAuthenticated
from schemas.graphql.user import (
    CreateUserInput,
    CreateUserResult,
    DeleteUserResult,
    UpdateUserInput,
    UpdateUserResult,
    UserError,
)
from schemas.pydantic.user import UserSchema
from services.user import add_user, deleted_user, updated_user


@type
class MutationUser:
    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def add_user(self, info: Info, user: CreateUserInput) -> CreateUserResult:
        try:
            user_data = UserSchema(
                email=user.email,
                password=user.password,
                full_name=user.full_name,
                rol=user.rol.value,
            )
            return add_user(info.context["db"], user_data)
        except UserDuplicated as e:
            return UserError(message=e.__str__())

    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def update_user(
        self, info: Info, user: UpdateUserInput
    ) -> UpdateUserResult:
        try:
            user_data = UserSchema(
                email=user.email,
                password=user.password,
                full_name=user.full_name,
                rol=user.rol.value if user.rol else None,
            )
            return updated_user(info.context["db"], user_data)
        except UserNotFound as e:
            return UserError(message=e.__str__())

    @mutation(permission_classes=[IsAuthenticated, IsAdmin])
    def delete_user(self, info: Info, email: str) -> DeleteUserResult:
        try:
            return deleted_user(info.context["db"], email)
        except UserNotFound as e:
            return UserError(message=e.__str__())
