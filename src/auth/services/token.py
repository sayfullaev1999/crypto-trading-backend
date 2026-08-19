from uuid import UUID

from redis.asyncio import Redis

from auth.exceptions import InvalidTokenError
from auth.services.jwt import JWTService


class TokenService:
    REFRESH_TOKEN_PREFIX = "auth:refresh:"

    def __init__(self, jwt_service: JWTService, redis: Redis) -> None:
        self.jwt_service = jwt_service
        self.redis = redis

    async def create_token_pair(self, user_id: UUID) -> tuple[str, str]:
        access_token = self.jwt_service.create_access_token(user_id=user_id)
        refresh_token = self.jwt_service.create_refresh_token(user_id=user_id)

        payload = self.jwt_service.decode_token(refresh_token)

        jti = payload.get("jti")

        if not jti:
            raise InvalidTokenError

        await self.redis.set(
            name=self._get_refresh_key(jti),
            value=str(user_id),
            ex=self.jwt_service.refresh_token_expire_seconds,
        )

        return access_token, refresh_token

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        payload = self._decode_refresh_token(refresh_token)

        jti = payload.get("jti")
        user_id = payload.get("sub")

        if not jti or not user_id:
            raise InvalidTokenError

        stored_user_id = await self.redis.get(self._get_refresh_key(jti))

        if stored_user_id != user_id:
            raise InvalidTokenError

        await self.redis.delete(self._get_refresh_key(jti))

        return await self.create_token_pair(user_id=UUID(user_id))

    async def revoke(self, refresh_token: str) -> None:
        payload = self._decode_refresh_token(refresh_token)

        jti = payload.get("jti")

        if not jti:
            raise InvalidTokenError

        await self.redis.delete(self._get_refresh_key(jti))

    def _decode_refresh_token(self, token: str) -> dict:
        try:
            payload = self.jwt_service.decode_token(token)
        except Exception as exc:
            raise InvalidTokenError from exc

        if payload.get("type") != "refresh":
            raise InvalidTokenError

        return payload

    def _get_refresh_key(self, jti: str) -> str:
        return f"{self.REFRESH_TOKEN_PREFIX}{jti}"
