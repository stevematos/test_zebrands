from datetime import datetime, timedelta

import bcrypt
from config.environment import JWT_ENCRYPT_ALGO, JWT_KEY, MINUTES_PER_SESSION
from pydantic import SecretStr
from utils.tokens import encode


def hash_password(password: SecretStr) -> str:
    decoded_bytes = bcrypt.hashpw(
        password.get_secret_value().encode(), bcrypt.gensalt()
    ).decode()
    return str(decoded_bytes)


def check_password_hash(password: SecretStr, hashed_password: str) -> bool:
    return bool(
        bcrypt.checkpw(
            password.get_secret_value().encode(), hashed_password.encode()
        )
    )


def create_jwt_with_params(
    email: str,
    user_id: int,
    min_per_session: float = MINUTES_PER_SESSION,
    secret_key: str = JWT_KEY,
):
    expiration = datetime.utcnow() + timedelta(minutes=min_per_session)

    payload = {
        "email": email,
        "user_id": user_id,
        "exp": expiration,
    }

    return encode(payload, secret_key, algorithm=JWT_ENCRYPT_ALGO)
