import RPi.GPIO as GPIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pin:
    """A class representing a GPIO pin."""

    def __init__(self, number: int, mode: str, pull_up_down: str = None):
        """Initialize a new Pin instance.

        Args:
            number (int): The number of the GPIO pin.
            mode (str): The mode of the GPIO pin (e.g., "OUT", "IN").
            pull_up_down (str, optional): The pull-up/pull-down resistor mode of the GPIO pin (e.g., "UP", "DOWN", None).
        """
        self.number = number
        self.mode = mode
        self.pull_up_down = pull_up_down

        # Set up the GPIO pin
        self.setup()

    def setup(self):
        """Set up the GPIO pin with the specified mode and pull-up/pull-down settings."""
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(self.number, GPIO.OUT if self.mode == "OUT" else GPIO.IN, pull_up_down=self.get_pull_up_down())
        logger.info(f"Pin {self.number} set to mode {self.mode} with pull-up/down {self.pull_up_down}.")

    def get_pull_up_down(self):
        """Convert pull-up/down string to GPIO constant."""
        if self.pull_up_down == "UP":
            return GPIO.PUD_UP
        elif self.pull_up_down == "DOWN":
            return GPIO.PUD_DOWN
        return GPIO.PUD_OFF

    def set_mode(self, mode: str):
        """Set the mode of the GPIO pin.

        Args:
            mode (str): The mode of the GPIO pin (e.g., "OUT", "IN").
        """
        self.mode = mode
        self.setup()  # Re-setup the pin with the new mode

    def set_state(self, state: bool):
        """Set the state of the GPIO pin.

        Args:
            state (bool): The state of the GPIO pin (True for high, False for low).
        """
        if self.mode == "OUT":
            GPIO.output(self.number, GPIO.HIGH if state else GPIO.LOW)
            logger.info(f"Pin {self.number} set to {'HIGH' if state else 'LOW'}.")
        else:
            raise ValueError("GPIO pin must be in OUT mode to set state")

    def get_state(self) -> bool:
        """Get the state of the GPIO pin.

        Returns:
            bool: The state of the GPIO pin (True for high, False for low).
        """
        if self.mode == "IN":
            state = GPIO.input(self.number)
            logger.info(f"Pin {self.number} state is {'HIGH' if state else 'LOW'}.")
            return state
        else:
            raise ValueError("GPIO pin must be in IN mode to get state")

    def cleanup(self):
        """Clean up the GPIO settings for this pin."""
        GPIO.cleanup(self.number)
        logger.info(f"Pin {self.number} cleaned up.")

# Example usage
if __name__ == "__main__":
    try:
        pin = Pin(number=17, mode="OUT")
        pin.set_state(True)  # Set pin 17 to HIGH
        pin.set_state(False)  # Set pin 17 to LOW

        pin.set_mode("IN")  # Change mode to input
        state = pin.get_state()  # Read the state of pin 17
        print(f"State of pin 17: {'HIGH' if state else 'LOW'}")
    finally:
        pin.cleanup()  # Ensure cleanup is called
