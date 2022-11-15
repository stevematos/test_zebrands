from pydantic import SecretStr
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from config.exceptions import UserDuplicated, UserNotFound
from models.users import User
from queries.user import (
    create_user,
    deactivate_user,
    get_user_by_email,
    update_user,
)
from schemas.graphql.user import (
    CreateUserResponse,
    DeleteUserResponse,
    UpdateUserResponse,
)
from schemas.pydantic.user import UserSchema
from utils.auth import hash_password
from utils.extras import clean_dict


def add_user(db: Session, user: UserSchema) -> CreateUserResponse:
    try:
        if get_user_by_email(db, user.email):
            raise UserDuplicated()
    except NoResultFound:
        pass

    create_data = user.__dict__
    create_data["hashed_password"] = hash_password(
        SecretStr(create_data.pop("password"))
    )

    db_user = create_user(db, User(**create_data))

    return CreateUserResponse(
        email=db_user.email,
        full_name=db_user.full_name,
        rol=db_user.rol.value,
    )


def updated_user(db: Session, user: UserSchema) -> UpdateUserResponse:
    try:
        user_data = get_user_by_email(db, user.email)
    except NoResultFound:
        raise UserNotFound()

    update_data = clean_dict(user.__dict__)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(
            SecretStr(update_data.pop("password"))
        )

    update_user(db, user_data.id, User(**update_data))
    return UpdateUserResponse(
        full_name=user_data.full_name, rol=user_data.rol.value
    )


def deleted_user(db: Session, email: str) -> DeleteUserResponse:
    try:
        user_data = get_user_by_email(db, email)
    except NoResultFound:
        raise UserNotFound()

    deactivate_user(db, user_data.id)
    return DeleteUserResponse(
        email=user_data.email,
        full_name=user_data.full_name,
        rol=user_data.rol.value,
        message="User deleted successfully",
    )
