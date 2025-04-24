# app/utils/mqtt_client.py
import asyncio
from datetime import datetime, timezone
import json
from aiomqtt import Client, MqttError
from sqlalchemy import select
from app.config import settings
from app.utils.logging_config import logger
from app.database import get_db
from app.models import Sensor, Reading, Command

class MQTTClient:
    def __init__(self):
        self.client = None
        self.connected = False
        
    async def connect(self):
        try:
            self.client = Client(
                hostname=settings.MQTT_BROKER,
                port=settings.MQTT_PORT,
                clean_session=True
            )
            await self.client.__aenter__()
            self.connected = True
            logger.info("Connected to MQTT broker")
            
            # Subscribe to actuator commands (for simulation)
            await self.client.subscribe(settings.MQTT_TOPIC_ACTUATORS_SUB)
            logger.info(f"Subscribed to {settings.MQTT_TOPIC_ACTUATORS_SUB}")
            await self.client.subscribe(settings.MQTT_TOPIC_SENSORS_SUB)
            logger.info(f"Subscribed to {settings.MQTT_TOPIC_SENSORS_SUB}")
            
        except MqttError as e:
            logger.error(f"MQTT connection error: {e}")
            await self.reconnect()

    async def reconnect(self):
        logger.info("Attempting MQTT reconnection...")
        await asyncio.sleep(5)
        await self.connect()

    async def publish(self, topic: str, payload: dict):
        try:
            await self.client.publish(
                topic, 
                payload=json.dumps(payload).encode(),
                qos=1
            )
        except MqttError as e:
            logger.error(f"Publish error: {e}")
            self.connected = False
            await self.reconnect()

    async def listen(self):
        # subscribe first…
        await self.client.subscribe(settings.MQTT_TOPIC_ACTUATORS_SUB)
        # then simply iterate the messages property
        async for message in self.client.messages:
            topic = message.topic.value
            payload = json.loads(message.payload.decode())
            logger.info(f"Received MQTT: {topic} - {payload}")
            
            # Handle simulated actuator responses
            if "actuators" in topic:
                logger.info(f"[SIMULATION] Actuator {topic} would execute: {payload}")
                await self.handle_actuator_ack(payload)
            
            if "sensors" in topic:
                await self.handle_sensor_reading(topic, payload)
    
    async def handle_sensor_reading(self, topic: str, payload: dict):
        
        sensor_id = int(topic.split("/")[-1])
        async for session in get_db():
            # Verify sensor exists
            result = await session.execute(select(Sensor).where(Sensor.id == sensor_id))
            if not result.scalars().first():
                return

            # Store reading
            reading = Reading(
                sensor_id=sensor_id,
                value=payload["value"]
            )
            session.add(reading)
            await session.commit()
    
    async def handle_actuator_ack(self, payload: dict):
        
        async for session in get_db():
            command: Command|None = await session.get(Command, payload["db_command_id"])
            if command:
                command.executed = True
                command.executed_at = datetime.now(timezone.utc)
                session.add(command)
                await session.commit()
                logger.info(f"Command {payload['db_command_id']} confirmed")

    async def disconnect(self):
        if self.connected:
            await self.client.__aexit__()
            self.connected = False
            logger.info("Disconnected from MQTT broker")

mqtt_client = MQTTClient()