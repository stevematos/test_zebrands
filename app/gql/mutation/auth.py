from config.exceptions import UserIncorrect, UserNotFound
from schemas.graphql.auth import LoginError, LoginResult, LoginSuccess
from services.auth import get_session_token
from strawberry import mutation, type
from strawberry.types import Info


@type
class MutationAuth:
    @mutation
    def login(self, info: Info, email: str, password: str) -> LoginResult:
        try:
            return LoginSuccess(
                session_token=get_session_token(
                    info.context["db"], email, password
                )
            )
        except (UserNotFound, UserIncorrect) as e:
            return LoginError(message=e.__str__())
