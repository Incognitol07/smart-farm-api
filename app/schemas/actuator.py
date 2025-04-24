# app/schemas/actuator.py

from pydantic import BaseModel
from app.utils.enums import ActuatorState


class ActuatorCommand(BaseModel):
    actuator_id: int
    command: ActuatorState = ActuatorState.OFF  # Default command is OFF

class ActuatorCreate(BaseModel):
    name: str
    state: ActuatorState = ActuatorState.OFF  # Default state is OFF