import os
import json
import logging
import asyncio
import aiohttp
import websockets
from aiohttp import ClientTimeout

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the cloud monitoring API endpoint and token from environment variables
MONITORING_API = os.getenv("MONITORING_API", "https://your_cloud_monitoring_service/api/metrics")
MONITORING_TOKEN = os.getenv("MONITORING_TOKEN", "your_cloud_monitoring_token")
MONITORING_WS = os.getenv("MONITORING_WS", "wss://your_cloud_monitoring_service/api/metrics/ws")

async def send_metric(metric_name, value):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {MONITORING_TOKEN}",
            "Content-Type": "application/json",
        }
        data = {
            "name": metric_name,
            "value": value,
        }
        retries = 5
        for attempt in range(retries):
            try:
                async with session.post(MONITORING_API, headers=headers, json=data, timeout=ClientTimeout(total=10)) as response:
                    response.raise_for_status()
                    logging.info(f"Sent metric: {metric_name} with value: {value}")
                    return
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed to send metric: {e}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logging.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    logging.error("Max retries reached. Could not send metric.")

async def listen_to_metrics():
    async with websockets.connect(MONITORING_WS) as websocket:
        # Authenticate if necessary
        await websocket.send(json.dumps({"type": "auth", "token": MONITORING_TOKEN}))
        response = await websocket.recv()
        logging.info(f"WebSocket Auth Response: {response}")

        # Listen for incoming metrics
        while True:
            try:
                message = await websocket.recv()
                logging.info(f"Received metric update: {message}")
                # Here you can add logic to process the incoming metrics
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                break

async def main():
    # Example usage
    await send_metric("cpu_usage", 75)
    await listen_to_metrics()

if __name__ == "__main__":
    asyncio.run(main())
