from schemas.graphql.auth import (
    LoginResult,
    LoginError,
    LoginSuccess,
)
from strawberry.types import Info
from strawberry import (
    type,
    mutation,
)

from services.auth import get_session_token
from config.exceptions import UserNotFound, UserIncorrect


@type
class MutationAuth:
    @mutation
    def login(self, info: Info, email: str, password: str) -> LoginResult:
        try:
            return LoginSuccess(session_token=get_session_token(info.context['db'], email, password))
        except (UserNotFound, UserIncorrect) as e:
            return LoginError(message=e)

