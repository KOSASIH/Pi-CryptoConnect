import RPi.GPIO as GPIO

# Initialize the GPIO library
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins to be used
PIN_1 = 17
PIN_2 = 27
PIN_3 = 22

# Set up the GPIO pins as outputs
GPIO.setup(PIN_1, GPIO.OUT)
GPIO.setup(PIN_2, GPIO.OUT)
GPIO.setup(PIN_3, GPIO.OUT)


def switch_on(pin):
    """Switch on a GPIO pin."""
    if pin in [PIN_1, PIN_2, PIN_3]:
        GPIO.output(pin, GPIO.HIGH)
    else:
        raise ValueError(f"Invalid pin number: {pin}")


def switch_off(pin):
    """Switch off a GPIO pin."""
    if pin in [PIN_1, PIN_2, PIN_3]:
        GPIO.output(pin, GPIO.LOW)
    else:
        raise ValueError(f"Invalid pin number: {pin}")


def get_state(pin):
    """Get the current state of a GPIO pin."""
    if pin in [PIN_1, PIN_2, PIN_3]:
        return GPIO.input(pin)
    else:
        raise ValueError(f"Invalid pin number: {pin}")
