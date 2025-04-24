# app/background_tasks/jobs/sensor_simulator.py
import asyncio
import json
import random
from aiomqtt import Client
from app.config import settings
from app.utils.logging_config import logger

async def simulate_sensors():
    """Publish fake sensor readings periodically"""
    async with Client(settings.MQTT_BROKER, settings.MQTT_PORT) as client:
        while True:
            await asyncio.sleep(55)  # Every 55 seconds
            
            # Simulate moisture sensor
            moisture = random.uniform(30.0, 70.0)
            await client.publish(f"{settings.MQTT_TOPIC_SENSORS_BASE}/1",
                payload=json.dumps({"value": moisture}),
                qos=1
            )
            
            # Simulate temperature sensor
            temp = random.uniform(18.0, 35.0)
            await client.publish(
                f"{settings.MQTT_TOPIC_SENSORS_BASE}/2",
                payload=json.dumps({"value": temp}),
                qos=1
            )
            
            logger.debug(f"Published simulated sensor data")