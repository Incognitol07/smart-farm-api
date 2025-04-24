# app/models/actuator.py

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import  relationship
from app.database import Base

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(50))  # moisture, temperature, etc
    location = Column(String(100))
    min_value = Column(Float)
    max_value = Column(Float)
    readings = relationship("Reading", back_populates="sensor")
