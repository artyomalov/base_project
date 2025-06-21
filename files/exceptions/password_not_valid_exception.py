class InvalidPasswordError(Exception):
    def __str__(self):
        return "Password is not valid"
