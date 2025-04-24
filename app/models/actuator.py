# app/models/actuator.py

from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import event
from app.database import Base
from app.models.command import Command
from app.utils.enums import ActuatorState

class Actuator(Base):
    __tablename__ = "actuators"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))  # pump, fan, etc
    state = Column(Enum(ActuatorState), default=ActuatorState.OFF)
    commands = relationship("Command", back_populates="actuator")


@event.listens_for(Command, 'after_update')
def command_status_listener(mapper, connection, target):
    """Update actuator state when command is executed"""
    if target.executed:
        connection.execute(
            Actuator.__table__.update()
            .where(Actuator.id == target.actuator_id)
            .values(state=target.command)
        )