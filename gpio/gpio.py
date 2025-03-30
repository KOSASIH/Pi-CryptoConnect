import RPi.GPIO as GPIO
import logging
from contextlib import contextmanager
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPIOController:
    """A class to control GPIO pins on a Raspberry Pi."""

    def __init__(self, pins: List[int]):
        """Initialize the GPIO controller with specified pins.

        Args:
            pins (List[int]): A list of GPIO pin numbers to control.
        """
        self.pins = pins
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        self.setup_pins()

    def setup_pins(self):
        """Set up the GPIO pins as outputs."""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            logger.info(f"Pin {pin} set as OUTPUT.")

    def switch_on(self, pin: int):
        """Switch on a GPIO pin.

        Args:
            pin (int): The GPIO pin number to switch on.
        """
        self._validate_pin(pin)
        GPIO.output(pin, GPIO.HIGH)
        logger.info(f"Pin {pin} switched ON.")

    def switch_off(self, pin: int):
        """Switch off a GPIO pin.

        Args:
            pin (int): The GPIO pin number to switch off.
        """
        self._validate_pin(pin)
        GPIO.output(pin, GPIO.LOW)
        logger.info(f"Pin {pin} switched OFF.")

    def toggle(self, pin: int):
        """Toggle the state of a GPIO pin.

        Args:
            pin (int): The GPIO pin number to toggle.
        """
        self._validate_pin(pin)
        current_state = GPIO.input(pin)
        new_state = GPIO.LOW if current_state == GPIO.HIGH else GPIO.HIGH
        GPIO.output(pin, new_state)
        logger.info(f"Pin {pin} toggled to {'ON' if new_state == GPIO.HIGH else 'OFF'}.")

    def get_state(self, pin: int) -> int:
        """Get the current state of a GPIO pin.

        Args:
            pin (int): The GPIO pin number to check.

        Returns:
            int: The current state of the pin (GPIO.HIGH or GPIO.LOW).
        """
        self._validate_pin(pin)
        state = GPIO.input(pin)
        logger.info(f"Pin {pin} state is {'ON' if state == GPIO.HIGH else 'OFF'}.")
        return state

    def _validate_pin(self, pin: int):
        """Validate if the pin is in the list of controlled pins.

        Args:
            pin (int): The GPIO pin number to validate.

        Raises:
            ValueError: If the pin is not valid.
        """
        if pin not in self.pins:
            raise ValueError(f"Invalid pin number: {pin}. Valid pins are: {self.pins}")

    def cleanup(self):
        """Clean up the GPIO settings."""
        GPIO.cleanup()
        logger.info("GPIO cleanup completed.")

    @contextmanager
    def manage_gpio(self):
        """Context manager for GPIO operations."""
        try:
            yield self
        finally:
            self.cleanup()

# Example usage
if __name__ == "__main__":
    pins = [17, 27, 22]
    with GPIOController(pins) as gpio:
        gpio.switch_on(17)
        gpio.switch_off(27)
        gpio.toggle(22)
        state = gpio.get_state(17)
        print(f"State of pin 17: {'ON' if state == GPIO.HIGH else 'OFF'}")
