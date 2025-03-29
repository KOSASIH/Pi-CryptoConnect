from celery import Celery
from time import sleep
import RPi.GPIO as GPIO
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Celery
celery = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'pyamqp://guest@localhost//'))

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

# Dynamically set GPIO pin from environment variable or default to 18
GPIO_PIN = int(os.getenv('GPIO_PIN', 18))
GPIO.setup(GPIO_PIN, GPIO.OUT)

@celery.task(bind=True)
def toggle_gpio(self):
    """Toggle the GPIO pin state."""
    try:
        current_state = GPIO.input(GPIO_PIN)
        GPIO.output(GPIO_PIN, not current_state)
        logging.info(f"Toggled GPIO pin {GPIO_PIN} to {'HIGH' if not current_state else 'LOW'}")
        sleep(1)
    except Exception as e:
        logging.error(f"Error toggling GPIO pin {GPIO_PIN}: {e}")
        self.retry(exc=e, countdown=5)  # Retry the task in case of failure

def cleanup_gpio():
    """Clean up GPIO settings on shutdown."""
    GPIO.cleanup()
    logging.info("GPIO cleanup completed.")

# Ensure GPIO cleanup on exit
import atexit
atexit.register(cleanup_gpio)
