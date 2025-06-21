class JWTTokenHasNotBeenProvidedError(Exception):

    def __str__(self):
        return f"JWT token has not been provided. Please provide a valid JWT token"
