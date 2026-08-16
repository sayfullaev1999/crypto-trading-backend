from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from auth.providers import AuthProvider
from infrastructure.database.providers import DatabaseProvider
from infrastructure.redis.providers import RedisProvider
from users.providers import UsersProvider
from wallets.providers import WalletProvider

container = make_async_container(
    FastapiProvider(),

    DatabaseProvider(),
    RedisProvider(),

    UsersProvider(),
    WalletProvider(),
    AuthProvider(),
)
