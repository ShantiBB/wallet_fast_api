from celery import Celery

from app.core.config import settings

celery_app = Celery("wallet_tasks")

celery_config = settings.celery.setup_celery_config
celery_app.conf.update(celery_config)

celery_app.autodiscover_tasks(['app.wallet.tasks'])
