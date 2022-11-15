from typing import Any

import jwt


def encode(
    payload: dict[str, Any],
    key: str,
    headers: dict[str, Any] | None = None,
    algorithm: str = "HS256",
) -> str:
    return jwt.encode(payload, key, headers=headers, algorithm=algorithm)


def decode(token: str, key, algorithm: str = "HS256") -> dict:
    return jwt.decode(token, key, algorithms=[algorithm])
