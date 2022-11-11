from sqlalchemy.orm import Session

from queries.auth import get_user_by_email
from utils.tokens import decode
import jwt
from datetime import datetime

from config.environment import config_env


def _validate_user(db: Session, payload: dict) -> bool:
    if not get_user_by_email(db, payload['email']):
        return False
    if datetime.utcnow().timestamp() >= payload['exp']:
        return False
    return True


def authenticate(db: Session, session_token: str) -> bool:
    try:
        decoded_jwt = decode(session_token, config_env().JWT_KEY)
    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError, jwt.InvalidSignatureError, jwt.DecodeError):
        return False

    if not _validate_user(db, decoded_jwt):
        return False

    return True
