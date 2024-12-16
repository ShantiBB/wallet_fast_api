from uuid import UUID
from decimal import Decimal

from celery import shared_task
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from app.wallet.models import Wallet
from app.core.database.db_helper import sync_database
from app.api.validations import WalletValidation


@shared_task(
    name='transaction_wallet_task',
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
    default_retry_delay=20
)
def transaction_wallet_task(
        wallet_id: UUID,
        operation_type: str,
        amount: Decimal
) -> dict[str, str]:
    with sync_database.session_factory() as db_session:
        balance = get_wallet_balance_by_id(
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
        db_session.execute(stmt)
        db_session.commit()

        return {'detail': f'Баланс кошелька {balance}'}


def get_wallet_balance_by_id(
    wallet_id: UUID,
    operation_type: str,
    amount: Decimal,
    db_session: Session
) -> Decimal:
    query = select(Wallet.balance).filter_by(id=wallet_id)
    result = db_session.execute(query)
    balance = result.scalar_one_or_none()

    WalletValidation.exist_obj(balance)
    WalletValidation.operation_type(operation_type)
    WalletValidation.balance(operation_type, amount, balance)

    return balance
