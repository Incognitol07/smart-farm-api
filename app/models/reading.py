# app/models/actuator.py

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship
from app.database import Base
from sqlalchemy.sql import func

class Reading(Base):
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(String, ForeignKey("sensors.id"))
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    sensor = relationship("Sensor", back_populates="readings")