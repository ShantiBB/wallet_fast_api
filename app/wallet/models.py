from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base
from app.core.database.mixins import IDMixin


class Wallet(Base, IDMixin):
    __tablename__ = "wallets"

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
