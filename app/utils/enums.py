# app/utils/enums.py

from enum import StrEnum

class ActuatorState(StrEnum):
    ON = "ON"
    OFF = "OFF"
    ERROR = "ERROR"
