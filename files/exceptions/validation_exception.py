class ValidationError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"Validation error: {self.message}"
        else:
            return "Provided data does not valid."
