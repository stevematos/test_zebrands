from unittest.mock import create_autospec, patch

import pytest
from config.constants import RolEnum
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from models import User
from services.permission import _is_admin, authenticate, is_admin
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    ("rol", "expected"),
    (
        (RolEnum.admin, True),
        (RolEnum.anonymous, False),
    ),
)
@patch("services.permission.get_user_by_email")
def test__is_admin(mock_get_user_by_email, rol, expected):
    db = create_autospec(Session)

    email = "test@example.com"
    mock_get_user_by_email.return_value = User(id=1, rol=rol)
    actual = _is_admin(db, email)

    mock_get_user_by_email.assert_called_once_with(db, email)

    assert expected == actual


@pytest.mark.parametrize(
    ("session_token", "email", "validate_user", "is_decode"),
    (
        ("test1234", "test@example.com", True, True),
        ("expiredToken", "test@example.com", True, False),
        ("InvalidSignatureToken", "test@example.com", True, False),
        ("DecodeErrorToken", "test@example.com", True, False),
        ("test1234", "test@example.com", False, True),
    ),
)
@patch("services.permission._validate_user")
@patch("services.permission.decode")
def test_authenticate(
    mock_decode,
    mock__validate_user,
    session_token,
    email,
    validate_user,
    is_decode,
):

    db = create_autospec(Session)

    context = {"db": db}

    decode_jwt = {"email": email, "user_id": 1, "exp": 1657777777}

    def get_decode_side_effect(session_token, key, **kwargs):
        if session_token == "test1234":
            return decode_jwt
        elif session_token == "expiredToken":
            raise ExpiredSignatureError
        elif session_token == "InvalidSignatureToken":
            raise InvalidSignatureError
        elif session_token == "DecodeErrorToken":
            raise DecodeError

    mock_decode.side_effect = get_decode_side_effect
    mock__validate_user.return_value = validate_user

    actual = authenticate(context, session_token)

    if not is_decode:
        expected = (False, {})
        mock__validate_user.assert_not_called()
    else:
        mock_decode.assert_called_once_with(session_token, "")
        mock__validate_user.assert_called_once_with(db, decode_jwt)

        if not validate_user:
            expected = (False, {})
        else:
            expected = (
                True,
                {
                    "email": decode_jwt["email"],
                    "user_id": decode_jwt["user_id"],
                },
            )

    assert expected == actual


@pytest.mark.parametrize(
    ("session_token", "email", "_is_admin_value", "is_decode"),
    (
        ("test1234", "test@example.com", True, True),
        ("expiredToken", "test@example.com", True, False),
        ("InvalidSignatureToken", "test@example.com", True, False),
        ("DecodeErrorToken", "test@example.com", True, False),
        ("test1234", "test@example.com", False, True),
    ),
)
@patch("services.permission._is_admin")
@patch("services.permission.decode")
def testis_admin(
    mock_decode,
    mock__is_admin,
    session_token,
    email,
    _is_admin_value,
    is_decode,
):

    db = create_autospec(Session)

    decode_jwt = {"email": email, "user_id": 1, "exp": 1657777777}

    def get_decode_side_effect(session_token, key, **kwargs):
        if session_token == "test1234":
            return decode_jwt
        elif session_token == "expiredToken":
            raise ExpiredSignatureError
        elif session_token == "InvalidSignatureToken":
            raise InvalidSignatureError
        elif session_token == "DecodeErrorToken":
            raise DecodeError

    mock_decode.side_effect = get_decode_side_effect
    mock__is_admin.return_value = _is_admin_value

    actual = is_admin(db, session_token)

    if not is_decode:
        expected = False
        mock__is_admin.assert_not_called()
    else:
        mock_decode.assert_called_once_with(session_token, "")
        mock__is_admin.assert_called_once_with(db, decode_jwt["email"])

        if not _is_admin_value:
            expected = False
        else:
            expected = True

    assert expected == actual
