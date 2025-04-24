# app/models/actuator.py

from sqlalchemy import Column, String, Enum, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import  relationship
from app.database import Base
from sqlalchemy.sql import func
from app.utils.enums import ActuatorState

class Command(Base):
    __tablename__ = "commands"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    actuator_id = Column(String, ForeignKey("actuators.id"))
    command = Column(Enum(ActuatorState), default=ActuatorState.OFF)  # Default command is OFF
    executed = Column(Boolean, default=False)
    executed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    actuator = relationship("Actuator", back_populates="commands")