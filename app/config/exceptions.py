class UserNotFound(Exception):
    def __str__(self):
        return "User not found"


class UserIncorrect(Exception):
    def __str__(self):
        return "User or Password Incorrect"


class UserDuplicated(Exception):
    def __str__(self):
        return "User already exists"


class ProductNotFound(Exception):
    def __init__(self, sku: str) -> None:
        self.sku = sku

    def __str__(self):
        return f"Product with sku {self.sku} not found"


class ProductDuplicated(Exception):
    def __init__(self, sku: str) -> None:
        self.sku = sku

    def __str__(self):
        return f"The product with sku {self.sku} already exists"
