
from pydantic import SecretStr

import bcrypt

from config.environment import config_env
from datetime import datetime, timedelta

from utils.tokens import encode, decode


def hash_password(password: SecretStr) -> str:
    """
    See https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python.
    This is pretty nifty--the salt is baked into the hash itself and doesn't need
    to be saved anywhere else. We decode the hash from unicode to back to plain
    text for DB compatibility
    """
    decoded_bytes = bcrypt.hashpw(
        password.get_secret_value().encode(), bcrypt.gensalt()
    ).decode()
    return str(decoded_bytes)


def check_password_hash(password: SecretStr, hashed_password: str) -> bool:
    """See documentation for hash_password"""
    return bool(
        bcrypt.checkpw(password.get_secret_value().encode(), hashed_password.encode())
    )


def create_jwt_with_params(
    email: str,
    min_per_session: float = config_env().MINUTES_PER_SESSION,
    secret_key: str = config_env().JWT_KEY,
):
    expiration = datetime.utcnow() + timedelta(minutes=min_per_session)
    payload = {
        "email": email,
        "exp": expiration,
    }
    return encode(
        payload, secret_key, algorithm=config_env().JWT_ENCRYPT_ALGO
    )


