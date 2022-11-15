from datetime import datetime

import jwt
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from strawberry.types import Info

from config.constants import RolEnum
from config.environment import JWT_KEY
from queries.user import get_user_by_email
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


def _save_data_info(info: Info, decoded_jwt: dict):
    info.context["email"] = decoded_jwt["email"]
    info.context["user_id"] = decoded_jwt["user_id"]


def _is_admin(db: Session, email: str) -> bool:
    if (
        user_data := get_user_by_email(db, email)
    ) and user_data.rol == RolEnum.admin:
        return True
    return False


def authenticate(info: Info, session_token: str) -> bool:
    try:
        decoded_jwt = decode(session_token, JWT_KEY)
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.InvalidSignatureError,
        jwt.DecodeError,
    ):
        return False

    if not _validate_user(info.context["db"], decoded_jwt):
        return False

    _save_data_info(info, decoded_jwt)

    return True


def is_admin(db: Session, session_token: str) -> bool:
    try:
        decoded_jwt = decode(session_token, JWT_KEY)
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.InvalidSignatureError,
        jwt.DecodeError,
    ):
        return False

    if not _is_admin(db, decoded_jwt["email"]):
        return False

    return True
