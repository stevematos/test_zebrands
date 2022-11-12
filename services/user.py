from pydantic import SecretStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.users import User
from queries.user import create_user, update_user, get_user_by_email
from schemas.graphql.user import CreateUserResponse, UpdateUserResponse
from schemas.pydantic.user import UserSchema
from utils.auth import hash_password
from utils.exceptions import UserDuplicated, UserNotFound


def add_user(db: Session, user: UserSchema) -> CreateUserResponse:
    try:
        if get_user_by_email(db, user.email):
            raise UserDuplicated()
    except NoResultFound:
        pass

    user.password = hash_password(SecretStr(user.password))
    db_user = create_user(db, User(
        email=user.email,
        hashed_password=user.password,
        full_name=user.full_name,
        rol=user.rol.value
    ))
    return CreateUserResponse(
        email=db_user.email,
        full_name=db_user.full_name,
        rol=db_user.rol.value
    )


def updated_user(db: Session, user: UserSchema) -> UpdateUserResponse:
    try:
        user_data = get_user_by_email(db, user.email)
    except NoResultFound:
        raise UserNotFound()

    db_user = update_user(db, user_data.id, User(
        email=user.email,
        full_name=user.full_name,
        rol=user.rol.value
    ))
    return UpdateUserResponse(
        full_name=db_user.full_name,
        rol=db_user.rol
    )
