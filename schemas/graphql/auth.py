from strawberry import type, union



@type
class LoginSuccess:
    session_token: str


@type
class LoginError:
    message: str


LoginResult = union("LoginResult", (LoginSuccess, LoginError))



