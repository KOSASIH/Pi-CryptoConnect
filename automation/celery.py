from celery import Celery
import os

# Initialize Celery
celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@localhost//'))

# Set up periodic tasks
celery.conf.beat_schedule = {
    'toggle-gpio-every-30-seconds': {
        'task': 'tasks.toggle_gpio',
        'schedule': 30.0,
    },
}

# Optional: Configure task result backend
celery.conf.result_backend = os.getenv('CELERY_RESULT_BACKEND', 'rpc://')
