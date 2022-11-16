from datetime import datetime

from config.constants import RolEnum
from config.environment import JWT_KEY
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from queries.user import get_user_by_email
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from utils.tokens import decode


def _validate_user(db: Session, payload: dict) -> bool:
    try:
        if not get_user_by_email(db, payload["email"]):
            return False
    except NoResultFound:
        return False

    if datetime.utcnow().timestamp() >= payload["exp"]:
        return False
    return True


def _save_data_info(decoded_jwt: dict):
    return {"email": decoded_jwt["email"], "user_id": decoded_jwt["user_id"]}


def _is_admin(db: Session, email: str) -> bool:
    if (
        user_data := get_user_by_email(db, email)
    ) and user_data.rol == RolEnum.admin:
        return True
    return False


def authenticate(context: dict, session_token: str) -> (bool, dict):
    try:
        decoded_jwt = decode(session_token, JWT_KEY)
    except (
        ExpiredSignatureError,
        InvalidSignatureError,
        DecodeError,
    ):
        return False, {}

    if not _validate_user(context["db"], decoded_jwt):
        return False, {}

    return True, _save_data_info(decoded_jwt)


def is_admin(db: Session, session_token: str) -> bool:
    try:
        decoded_jwt = decode(session_token, JWT_KEY)
    except (
        ExpiredSignatureError,
        InvalidSignatureError,
        DecodeError,
    ):
        return False

    if not _is_admin(db, decoded_jwt["email"]):
        return False

    return True
