from strawberry import type, union
# from schemas.graphql.user import TokenSchema


@type
class LoginSuccess:
    session_token: str


@type
class LoginError:
    message: str


LoginResult = union("LoginResult", (LoginSuccess, LoginError))



