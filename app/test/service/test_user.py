from unittest.mock import create_autospec, patch

import pytest
from config.constants import RolEnum
from config.exceptions import UserDuplicated
from models.users import User
from pydantic import SecretStr
from schemas.graphql.user import CreateUserResponse
from schemas.pydantic.user import UserSchema
from services.user import add_user
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    ("email", "is_duplicated"),
    (
        ("test@example.com", False),
        ("NoResultFound@example.com", False),
        ("duplicate@example.com", True),
    ),
)
@patch("services.user.create_user")
@patch("services.user.hash_password")
@patch("services.user.get_user_by_email")
def test_add_user(
    mock_get_user_by_email,
    mock_hash_password,
    mock_create_user,
    email,
    is_duplicated,
):
    db = create_autospec(Session)

    password = "test123"
    hashed_password = "hashedPassword"
    full_name = "John Doe"

    user = UserSchema(email=email, password=password)

    def get_user_by_email_effect(db, email, **kwargs):
        if email == "test@example.com":
            return None
        elif email == "duplicate@example.com":
            return User(email="test@example.com")
        elif email == "NoResultFound@example.com":
            raise NoResultFound()

    mock_get_user_by_email.side_effect = get_user_by_email_effect
    mock_hash_password.return_value = hashed_password

    mock_create_user.return_value = User(
        email=email, full_name=full_name, rol=RolEnum.admin
    )

    if is_duplicated:
        with pytest.raises(UserDuplicated):
            add_user(db, user)
    else:
        actual = add_user(db, user)

        mock_get_user_by_email.assert_called_once_with(db, email)
        mock_hash_password.assert_called_once_with(SecretStr(password))
        expected = CreateUserResponse(
            email=email, full_name=full_name, rol=RolEnum.admin.value
        )

        assert expected == actual
