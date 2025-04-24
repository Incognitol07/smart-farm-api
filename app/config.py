# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Smart Farm API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite+aiosqlite:///./smart_farm.db"
    
    # MQTT Configuration
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_TOPIC_SENSORS_BASE: str = "farm/sensors" 
    MQTT_TOPIC_SENSORS_SUB: str = MQTT_TOPIC_SENSORS_BASE + "/+"
    MQTT_TOPIC_ACTUATORS: str = "farm/actuators"
    MQTT_TOPIC_ACTUATORS_SUB: str = MQTT_TOPIC_ACTUATORS + "/+"

    class Config:
        env_file = ".env"

settings = Settings()