from decimal import Decimal
from uuid import UUID

from sqlalchemy import select, update, delete

from app.core.database.db_helper import AsyncSessionDep
from app.wallet.models import Wallet
from app.wallet.tasks import transaction_wallet_task
from app.api.validations import WalletValidation
from app.wallet.schemas import (
    WalletListSchema,
    WalletSchema,
    WalletCreateSchema
)


class WalletCRUD:

    def __init__(self, db_session: AsyncSessionDep = None):
        self.db_session = db_session

    async def list(self) -> WalletListSchema:
        query = select(
            Wallet.id,
            Wallet.title,
            Wallet.balance
        )

        result = await self.db_session.execute(query)
        wallets = result.fetchall()

        return wallets

    async def create(self, data: WalletCreateSchema,) -> Wallet:
        wallet = Wallet(**data.model_dump())

        self.db_session.add(wallet)
        await self.db_session.commit()

        return wallet

    async def get_by_id(self, wallet_id: UUID,) -> WalletSchema:
        query = select(Wallet).filter_by(id=wallet_id)

        result = await self.db_session.execute(query)
        wallet = result.scalars().one_or_none()

        WalletValidation.exist_obj(wallet)

        return wallet

    async def update_by_id(
        self,
        wallet_id: UUID,
        data: WalletCreateSchema
    ) -> WalletSchema:
        query = select(Wallet).filter_by(id=wallet_id)
        result = await self.db_session.execute(query)
        wallet = result.scalar_one_or_none()

        WalletValidation.exist_obj(wallet)
        WalletValidation.title_description(
            cur_title=wallet.title,
            new_title=data.title,
            cur_description=wallet.description,
            new_description=data.description
        )

        stmt = update(Wallet).filter_by(id=wallet.id).values(
            title=data.title,
            description=data.description
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return wallet

    async def delete_by_id(self, wallet_id: UUID) -> None:
        query = select(Wallet.id).filter_by(id=wallet_id)
        result = await self.db_session.execute(query)
        wallet_id = result.scalar_one_or_none()

        WalletValidation.exist_obj(wallet_id)

        stmt = delete(Wallet).filter_by(id=wallet_id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    @staticmethod
    async def get_wallet_balance_by_id(
            wallet_id: UUID,
            db_session: AsyncSessionDep
    ) -> Decimal:
        query = select(Wallet.balance).filter_by(id=wallet_id)
        result = await db_session.execute(query)
        balance = result.scalar_one_or_none()

        return balance

    async def create_transaction(
        self,
        wallet_id: UUID,
        operation_type: str,
        amount: Decimal,
        db_session: AsyncSessionDep
    ) -> dict[str, str]:

        balance = await self.get_wallet_balance_by_id(
            wallet_id=wallet_id,
            db_session=db_session
        )

        WalletValidation.exist_obj(balance)
        WalletValidation.operation_type(operation_type)
        WalletValidation.balance(operation_type, amount, balance)

        transaction_wallet_task.delay(
            wallet_id=wallet_id,
            balance=balance,
            operation_type=operation_type,
            amount=amount
        )

        return {'status': 'Success'}
