# tasks.py
from time import sleep

import RPi.GPIO as GPIO
from celery import Celery

# Initialize Celery
celery = Celery("tasks", broker="pyamqp://guest@localhost//")

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


@celery.task
def toggle_gpio():
    GPIO.output(18, not GPIO.input(18))
    sleep(1)


# celery.py

# Initialize Celery
celery = Celery("tasks", broker="pyamqp://guest@localhost//")

# Set up periodic tasks
celery.conf.beat_schedule = {
    "toggle-gpio-every-30-seconds": {
        "task": "tasks.toggle_gpio",
        "schedule": 30.0,
    },
}
