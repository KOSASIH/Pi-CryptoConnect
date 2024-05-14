import time


def collect_metrics():
    """Collect metrics related to the GPIO pins."""
    metrics = {
        "gpio_pin_1_state": get_state(PIN_1),
        "gpio_pin_2_state": get_state(PIN_2),
        "gpio_pin_3_state": get_state(PIN_3),
        "gpio_pin_1_on_count": get_on_count(PIN_1),
        "gpio_pin_2_on_count": get_on_count(PIN_2),
        "gpio_pin_3_on_count": get_on_count(PIN_3),
    }
    return metrics


def get_on_count(pin):
    """Get the number of times a GPIO pin has been switched on."""
    if pin in [PIN_1, PIN_2, PIN_3]:
        state_history = get_state_history(pin)
        on_count = sum(1 for state in state_history if state)
        return on_count
    else:
        raise ValueError(f"Invalid pin number: {pin}")


def get_state_history(pin):
    """Get the history of states for a GPIO pin."""
    # TODO: Implement this function
    pass
