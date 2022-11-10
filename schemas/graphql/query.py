from strawberry import type, field
from

@type
class Query:
    @field
    def user(self) -> User:
        return User(name="Patrick", age=100)
