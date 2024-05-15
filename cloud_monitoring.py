# home_assistant.py
import json

import requests

# Define the Home Assistant API endpoint
HASS_API = "http://localhost:8123/api/states"
HASS_TOKEN = "your_home_assistant_token"

# Define the Pi-CryptoConnect sensor entity
SENSOR_NAME = "pi_crypto_connect"


def update_sensor_state(state):
    # Make a request to the Home Assistant API to update the sensor state
    headers = {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "content-type": "application/json",
    }
    data = {
        "entity_id": f"sensor.{SENSOR_NAME}",
        "state": state,
    }
    response = requests.put(HASS_API, headers=headers, data=json.dumps(data))
    response.raise_for_status()


# cloud_monitoring.py

# Define the cloud monitoring API endpoint
MONITORING_API = "https://your_cloud_monitoring_service/api/metrics"
MONITORING_TOKEN = "your_cloud_monitoring_token"


def send_metric(metric_name, value):
    # Make a request to the cloud monitoring API to send a metric
    headers = {
        "Authorization": f"Bearer {MONITORING_TOKEN}",
        "content-type": "application/json",
    }
    data = {
        "name": metric_name,
        "value": value,
    }
    response = requests.post(MONITORING_API, headers=headers, data=json.dumps(data))
    response.raise_for_status()
