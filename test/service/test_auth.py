from unittest.mock import create_autospec, patch

import pytest
from pydantic import SecretStr
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from config.exceptions import UserIncorrect, UserNotFound
from models import User
from services.auth import get_session_token


@pytest.mark.parametrize(
    ("user_data", "email", "password", "check_password"),
    (
        (
            {
                "id": 1,
                "hashed_password": "TEST1234ASS",
            },
            "test@example.com",
            "test",
            True,
        ),
        (
            {
                "id": 1,
                "hashed_password": "TEST1234ASS",
            },
            "test@example.com",
            "test",
            False,
        ),
        (
            {},
            "fake@example.com",
            "test",
            True,
        ),
    ),
)
@patch("services.auth.create_jwt_with_params")
@patch("services.auth.check_password_hash")
@patch("services.auth.get_user_by_email")
def test_get_session_token(
    mock_get_user_by_email,
    mock_check_password_hash,
    mock_create_jwt_with_params,
    user_data,
    email,
    password,
    check_password,
):
    db = create_autospec(Session)

    mock_get_user_by_email.return_value = User(
        id=user_data.get("id"),
        hashed_password=user_data.get("hashed_password"),
    )
    mock_check_password_hash.return_value = check_password

    def get_user_by_email_side_effect(db, email, **kwargs):
        if email == "test@example.com":
            return User(
                id=user_data.get("id"),
                hashed_password=user_data.get("hashed_password"),
            )
        else:
            raise NoResultFound

    mock_get_user_by_email.side_effect = get_user_by_email_side_effect

    if not user_data:
        with pytest.raises(UserNotFound):
            get_session_token(db, email, password)
    elif not check_password:
        with pytest.raises(UserIncorrect):
            get_session_token(db, email, password)
    else:
        get_session_token(db, email, password)
        mock_get_user_by_email.assert_called_once_with(db, email)

        mock_check_password_hash.assert_called_once_with(
            SecretStr(password), user_data["hashed_password"]
        )

        mock_create_jwt_with_params.assert_called_once_with(
            email, user_data["id"]
        )
