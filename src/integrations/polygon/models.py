import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel


class PolygonMapping(BaseModel):
    __tablename__ = "polygon_mappings"

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
    api_ticker: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    ws_ticker: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
