import os
import json
import logging
import asyncio
import aiohttp
import websockets
import time
from aiohttp import ClientTimeout

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the Home Assistant API endpoint and token from environment variables
HASS_API = os.getenv("HASS_API", "http://localhost:8123/api/states")
HASS_TOKEN = os.getenv("HASS_TOKEN", "your_home_assistant_token")
HASS_WS = os.getenv("HASS_WS", "ws://localhost:8123/api/websocket")

# Define the Pi-CryptoConnect sensor entity
SENSOR_NAME = "pi_crypto_connect"

async def update_sensor_state(state):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {HASS_TOKEN}",
            "Content-Type": "application/json",
        }
        data = {
            "entity_id": f"sensor.{SENSOR_NAME}",
            "state": state,
        }
        retries = 5
        for attempt in range(retries):
            try:
                async with session.put(HASS_API, headers=headers, json=data, timeout=ClientTimeout(total=10)) as response:
                    response.raise_for_status()
                    logging.info(f"Updated sensor state to: {state}")
                    return
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed to update sensor state: {e}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error("Max retries reached. Could not update sensor state.")

async def listen_to_updates():
    async with websockets.connect(HASS_WS) as websocket:
        await websocket.send(json.dumps({"id": 1, "type": "auth", "access_token": HASS_TOKEN}))
        response = await websocket.recv()
        logging.info(f"WebSocket Auth Response: {response}")

        # Listen for updates
        while True:
            try:
                message = await websocket.recv()
                logging.info(f"Received update: {message}")
                # Here you can add logic to process the incoming updates
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                break

async def main():
    # Example usage
    await update_sensor_state("online")
    await listen_to_updates()

if __name__ == "__main__":
    asyncio.run(main())
