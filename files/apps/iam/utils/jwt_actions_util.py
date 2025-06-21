import jwt
from config import settings


class JWTActionsUtil:
    def __init__(
        self,
        private_key: str,
        public_key: str,
        algorithm: str,
    ):
        self.private_key = private_key
        self.algorithm = algorithm
        self.public_key = public_key

    def encode_jwt(self, payload: dict):
        encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)

        return encoded

    def decode_jwt(
        self,
        token: str | bytes,
    ) -> dict[str, str]:
        decoded = jwt.decode(
            token,
            self.public_key,
            algorithms=[
                self.algorithm,
            ],
        )

        return decoded


jwt_actions_util = JWTActionsUtil(
    private_key=settings.auth_jwt.PRIVATE_KEY_PATH.read_text(),
    public_key=settings.auth_jwt.PUBLIC_KEY_PATH.read_text(),
    algorithm=settings.auth_jwt.ALGORITHM,
)
