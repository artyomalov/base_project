class UnprocessableEntityError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"Unprocessable entity error: {self.message}"
        else:
            return "Unprocessable entity error: provided data is not valid."
