from celery import Celery

from app.config import settings

celery = Celery("tasks", broker=settings.BROKER_CELERY, include="app.tasks.tasks")
# celery -A app.tasks.celery:celery worker --loglevel=INFO --pool=solo
# celery -A app.tasks.celery:celery flower
