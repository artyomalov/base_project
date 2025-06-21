class IsNotActiveError(Exception):

    def __str__(self):
        return "User has been disabled."
