from uuid import UUID
from decimal import Decimal

from celery import shared_task
from sqlalchemy import update

from app.wallet.models import Wallet
from app.core.database.db_helper import sync_database


@shared_task(
    name='transaction_wallet_task',
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
    default_retry_delay=20
)
def transaction_wallet_task(
        wallet_id: UUID,
        balance: Decimal,
        operation_type: str,
        amount: Decimal
) -> dict[str, str]:
    with sync_database.session_factory() as db_session:
        if operation_type == 'deposit':
            balance += amount
        else:
            balance -= amount

        stmt = update(Wallet).filter_by(id=wallet_id).values(balance=balance)
        db_session.execute(stmt)
        db_session.commit()

        return {'detail': f'Баланс кошелька {balance}'}
