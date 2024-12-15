from typing import Any
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update, delete

from app.core.database import SessionDep
from app.wallet.models import Wallet
from app.wallet.schemas import (
    WalletListSchema,
    WalletSchema,
    WalletCreateSchema
)
from app.api.validations import (
    valid_exist_obj,
    valid_operation_type,
    valid_balance,
    valid_title_description
)


async def list_wallet(db_session: SessionDep) -> WalletListSchema:
    query = select(
        Wallet.id,
        Wallet.title,
        Wallet.balance
    )

    result = await db_session.execute(query)
    wallets = result.fetchall()

    return wallets


async def add_wallet(
    data: WalletCreateSchema,
    db_session: SessionDep
) -> Wallet:
    wallet = Wallet(**data.model_dump())

    db_session.add(wallet)
    await db_session.commit()

    return wallet


async def get_wallet_by_id(
        wallet_id: UUID,
        db_session: SessionDep
) -> WalletSchema:
    query = select(Wallet).filter_by(id=wallet_id)

    result = await db_session.execute(query)
    wallet = result.scalars().one_or_none()

    valid_exist_obj(wallet)

    return wallet


async def update_wallet_by_id(
    wallet_id: UUID,
    data: WalletCreateSchema,
    db_session: SessionDep
) -> WalletSchema:
    query = select(Wallet).filter_by(id=wallet_id)
    result = await db_session.execute(query)
    wallet = result.scalar_one_or_none()

    valid_exist_obj(wallet)
    valid_title_description(
        cur_title=wallet.title,
        new_title=data.title,
        cur_description=wallet.description,
        new_description=data.description
    )

    stmt = update(Wallet).filter_by(id=wallet.id).values(
        title=data.title,
        description=data.description
    )
    await db_session.execute(stmt)
    await db_session.commit()

    return wallet


async def delete_wallet_by_id(
    wallet_id: UUID,
    db_session: SessionDep
) -> None:
    query = select(Wallet.id).filter_by(id=wallet_id)
    result = await db_session.execute(query)
    wallet_id = result.scalar_one_or_none()

    valid_exist_obj(wallet_id)

    stmt = delete(Wallet).filter_by(id=wallet_id)
    await db_session.execute(stmt)
    await db_session.commit()


async def get_wallet_balance_by_id(
    wallet_id: UUID,
    operation_type: str,
    amount: Decimal,
    db_session: SessionDep
) -> Decimal:
    query = select(Wallet.balance).filter_by(id=wallet_id)
    result = await db_session.execute(query)
    balance = result.scalar_one_or_none()

    valid_exist_obj(balance)
    valid_operation_type(operation_type)
    valid_balance(operation_type, amount, balance)

    return balance


async def create_transaction_wallet(
        wallet_id: UUID,
        dict_data: dict[str, Any],
        operation_type: str,
        amount: Decimal,
        db_session: SessionDep
) -> dict[str, str]:
    balance = await get_wallet_balance_by_id(
        wallet_id=wallet_id,
        operation_type=operation_type,
        amount=amount,
        db_session=db_session
    )

    if operation_type == 'deposit':
        balance += amount
    else:
        balance -= amount

    stmt = update(Wallet).filter_by(id=wallet_id).values(balance=balance)
    await db_session.execute(stmt)
    await db_session.commit()

    return {'detail': f'Баланс кошелька {balance}'}
