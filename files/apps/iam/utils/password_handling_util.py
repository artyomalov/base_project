import bcrypt


class PasswordHandlingUtil:
    @classmethod
    def hash_password(cls, password: str | bytes) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes: bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    @classmethod
    def validate_password(cls, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"), hashed_password=hashed_password
        )
