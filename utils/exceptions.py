class UserNotFound(Exception):
    def __str__(self):
        return "User not found"


class UserIncorrect(Exception):
    def __str__(self):
        return "User or Password Incorrect"


class UserDuplicated(Exception):
    def __str__(self):
        return "User already exists"
