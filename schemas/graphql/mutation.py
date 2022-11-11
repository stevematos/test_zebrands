from strawberry import type, field

from sqlalchemy.orm.exc import NoResultFound
from queries.auth import get_user_by_email
from strawberry.types import Info
from pydantic import SecretStr

from schemas.graphql.auth import (
    LoginResult,
    LoginError,
    LoginSuccess,
)
from schemas.graphql.permission import IsAuthenticated
from utils.auth import check_password_hash, create_jwt_with_params


@type
class Mutation:
    @field
    def login(self, info: Info, email: str, password: str) -> LoginResult:
        try:
            user = get_user_by_email(info.context['db'], email)
        except NoResultFound:
            return LoginError(m54essage="User not found")

        if not check_password_hash(
            SecretStr(password), user.hashed_password
        ):
            return LoginError(message="User or Password Incorrect")

        return LoginSuccess(session_token=create_jwt_with_params(email))

    @field(permission_classes=[IsAuthenticated])
    def add_product(self, info: Info, sku: str) -> LoginSuccess:
        return LoginSuccess(session_token="str")
