from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from auth.providers import AuthProvider
from infrastructure.database.providers import DatabaseProvider
from infrastructure.redis.providers import RedisProvider
from integrations.binance.providers import BinanceProvider
from integrations.polygon.providers import PolygonProvider
from market_data.providers import MarketDataProvider
from symbols.providers import SymbolProvider
from users.providers import UsersProvider
from wallets.providers import WalletProvider


app_container = make_async_container(
    FastapiProvider(),

    DatabaseProvider(),
    RedisProvider(),

    UsersProvider(),
    WalletProvider(),
    AuthProvider(),
    SymbolProvider(),
    MarketDataProvider()
)

worker_container = make_async_container(
    DatabaseProvider(),
    RedisProvider(),

    BinanceProvider(),
    PolygonProvider(),
)
