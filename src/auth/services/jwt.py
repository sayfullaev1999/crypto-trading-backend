import uuid
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt


class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_seconds: int,
        refresh_token_expire_seconds: int,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_seconds = access_token_expire_seconds
        self.refresh_token_expire_seconds = refresh_token_expire_seconds

    def create_access_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=self.access_token_expire_seconds),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "jti": str(uuid4()),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(seconds=self.refresh_token_expire_seconds),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )
