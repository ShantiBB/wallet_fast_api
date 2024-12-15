from uuid import uuid4
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.database.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    title: Mapped[str] = mapped_column(
        String(100)
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=0
    )
