from pydantic import SecretStr

from utils.auth import check_password_hash, hash_password


def test_password_hashing():
    password = SecretStr("test")

    hash_1 = hash_password(password)
    hash_2 = hash_password(password)

    assert hash_1 != hash_2

    assert check_password_hash(password, hash_1)
    assert check_password_hash(password, hash_2)
