from typing import Literal

from pydantic import BaseModel


class MarketDataSubscription(BaseModel):
    action: Literal["subscribe", "unsubscribe"]
    symbols: list[str]
