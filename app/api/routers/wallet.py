from uuid import UUID

from starlette import status
from fastapi import APIRouter

from app.core.database.db_helper import AsyncSessionDep
from app.wallet.controllers import WalletCRUD
from app.wallet.schemas import (
    WalletCreateSchema,
    WalletSchema,
    WalletListSchema,
    TransactionSchema
)

router = APIRouter(
    prefix='/wallets',
    tags=['Кошельки']
)


@router.get(
    path="",
    summary='Получить список кошельков',
    status_code=status.HTTP_200_OK
)
async def list_wallets_view(
        db_session: AsyncSessionDep
) -> list[WalletListSchema]:
    wallet_crud = WalletCRUD(db_session)
    return await wallet_crud.list()


@router.get(
    path="/{wallet_id}",
    summary='Получить кошелёк по id',
    status_code=status.HTTP_200_OK
)
async def get_wallet_view(
    wallet_id: UUID,
    db_session: AsyncSessionDep
) -> WalletSchema:
    wallet_crud = WalletCRUD(db_session)
    return await wallet_crud.get_by_id(wallet_id)


@router.post(
    path="",
    summary='Добавить новый кошелёк',
    status_code=status.HTTP_201_CREATED
)
async def create_wallet_view(
    data: WalletCreateSchema,
    db_session: AsyncSessionDep
) -> WalletSchema:
    wallet_crud = WalletCRUD(db_session)
    wallet = await wallet_crud.create(data)

    return WalletSchema(
        id=wallet.id,
        title=wallet.title,
        description=wallet.description,
        balance=wallet.balance
    )


@router.put(
    path="/{wallet_id}",
    summary='Обновить кошелёк',
    status_code=status.HTTP_200_OK
)
async def update_wallet_view(
    wallet_id: UUID,
    data: WalletCreateSchema,
    db_session: AsyncSessionDep
) -> WalletSchema:
    wallet_crud = WalletCRUD(db_session)
    return await wallet_crud.update_by_id(
        wallet_id=wallet_id,
        data=data,
    )


@router.delete(
    path="/{wallet_id}",
    summary='Удалить кошелёк',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_wallet_view(
    wallet_id: UUID,
    db_session: AsyncSessionDep
) -> None:
    wallet_crud = WalletCRUD(db_session)
    await wallet_crud.delete_by_id(wallet_id)


@router.post(
    path="/{wallet_id}/operation",
    summary='Увеличить или уменьшить баланс кошелька',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_wallet_balance_view(
    wallet_id: UUID,
    data: TransactionSchema,
    db_session: AsyncSessionDep
) -> dict[str, str]:
    dict_data = data.model_dump()
    operation_type = dict_data.get('operation_type')
    amount = dict_data.get('amount')

    wallet_crud = WalletCRUD()
    return await wallet_crud.create_transaction(
        wallet_id=wallet_id,
        operation_type=operation_type,
        amount=amount,
        db_session=db_session
    )
