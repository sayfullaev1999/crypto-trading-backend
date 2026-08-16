import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import BaseModel

if TYPE_CHECKING:
    from users.models import User


class Wallet(BaseModel):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    user: Mapped["User"] = relationship(
        back_populates="wallet"
    )
    address: Mapped[str] = mapped_column(
        String(42),
        unique=True,
        nullable=False
    )
    encrypted_private_key: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
