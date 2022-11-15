from pydantic import SecretStr
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from config.exceptions import UserIncorrect, UserNotFound
from queries.user import get_user_by_email
from utils.auth import check_password_hash, create_jwt_with_params


def get_session_token(db: Session, email: str, password: str) -> str:
    try:
        user = get_user_by_email(db, email)
    except NoResultFound:
        raise UserNotFound()
    if not check_password_hash(SecretStr(password), user.hashed_password):
        raise UserIncorrect()

    return create_jwt_with_params(email, user.id)
