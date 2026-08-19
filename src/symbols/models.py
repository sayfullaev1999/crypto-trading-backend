import uuid

from sqlalchemy import UUID, String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import BaseModel
from symbols.enums import SymbolType


class Symbol(BaseModel):
    __tablename__ = "symbols"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    ticker: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    type: Mapped[SymbolType] = mapped_column(
        Enum(
            SymbolType,
            values_callable=lambda t: [item.value for item in t]
        ),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
