from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class WalletListSchema(BaseModel):
    id: UUID
    title: str
    balance: Decimal



class WalletSchema(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    balance: Decimal


class WalletCreateSchema(BaseModel):
    title: str
    description: str | None = None


class TransactionSchema(BaseModel):
    operation_type: str
    amount: Decimal
