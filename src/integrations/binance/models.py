import uuid

from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel


class BinanceMapping(BaseModel):
    __tablename__ = "binance_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    symbol_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("symbols.id"),
        nullable=False,
        unique=True
    )
    ticker: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
