from uuid import UUID

from starlette import status
from fastapi import APIRouter

from app.core.database import SessionDep
from app.wallet.controllers import (
    list_wallet,
    add_wallet,
    get_wallet_by_id,
    update_wallet_by_id,
    delete_wallet_by_id,
    create_transaction_wallet
)
from app.wallet.schemas import (
    WalletCreateSchema,
    WalletSchema,
    WalletListSchema,
    TransactionSchema
)

router = APIRouter(
    prefix='/api/v1',
    tags=['Кошельки']
)


@router.get(
    path="/wallets/",
    summary='Получить список кошельков',
    status_code=status.HTTP_200_OK
)
async def list_wallets_view(db_session: SessionDep) -> list[WalletListSchema]:
    return await list_wallet(db_session)


@router.get(
    path="/wallets/{wallet_id}/",
    summary='Получить кошелёк по id',
    status_code=status.HTTP_200_OK
)
async def get_wallet_view(
    wallet_id: UUID,
    db_session: SessionDep
) -> WalletSchema:
    return await get_wallet_by_id(wallet_id, db_session)


@router.post(
    path="/wallets/",
    summary='Добавить новый кошелёк',
    status_code=status.HTTP_201_CREATED
)
async def create_wallet_view(
    data: WalletCreateSchema,
    db_session: SessionDep
) -> WalletSchema:
    wallet = await add_wallet(data, db_session)

    return WalletSchema(
        id=wallet.id,
        title=wallet.title,
        description=wallet.description,
        balance=wallet.balance
    )


@router.put(
    path="/wallets/{wallet_id}/",
    summary='Обновить кошелёк',
    status_code=status.HTTP_200_OK
)
async def update_wallet_view(
    wallet_id: UUID,
    data: WalletCreateSchema,
    db_session: SessionDep
) -> WalletSchema:
    return await update_wallet_by_id(
        wallet_id=wallet_id,
        data=data,
        db_session=db_session
    )


@router.delete(
    path="/wallets/{wallet_id}/",
    summary='Удалить кошелёк',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wallet_view(
    wallet_id: UUID,
    db_session: SessionDep
) -> None:
    await delete_wallet_by_id(wallet_id, db_session)


@router.post(
    path="/wallets/{wallet_id}/operation/",
    summary='Увеличить или уменьшить баланс кошелька',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_wallet_balance_view(
    wallet_id: UUID,
    data: TransactionSchema,
    db_session: SessionDep
) -> dict[str, str]:
    dict_data = data.model_dump()
    operation_type = dict_data.get('operation_type')
    amount = dict_data.get('amount')

    return await create_transaction_wallet(
        wallet_id=wallet_id,
        dict_data=dict_data,
        operation_type=operation_type,
        amount=amount,
        db_session=db_session
    )
