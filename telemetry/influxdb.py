from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Initialize the InfluxDB client
client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

def write_metrics(metrics):
    """Write metrics to an InfluxDB database."""
    # Create a point for each metric
    points = [
        Point("gpio_pin_state").tag("pin", "1").field("state", metrics["gpio_pin_1_state"]),
        Point("gpio_pin_state").tag("pin", "2").field("state", metrics["gpio_pin_2_state"]),
        Point("gpio_pin_state").tag("pin", "3").field("state", metrics["gpio_pin_3_state"]),
        Point("gpio_pin_on_count").tag("pin", "1").field("count", metrics["gpio_pin_1_on_count"]),
        Point("gpio_pin_on_count").tag("pin", "2").field("count", metrics["gpio_pin_2_on_count"]),
        Point("gpio_pin_on_count").tag("pin", "3").field("count", metrics["gpio_pin_3_on_count"]),
    ]

    # Write the points to the InfluxDB database
    write_api.write(bucket="my-bucket", record=points)

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
