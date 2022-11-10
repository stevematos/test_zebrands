from strawberry import type


@strawberry.type
class User:
    name: str
    age: int