# app/routers/sensors.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Sensor, Reading
from app.schemas.sensor import SensorReading, SensorCreate

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.post("/")
async def create_sensor(payload: SensorCreate, db: AsyncSession = Depends(get_db)):
    sensor = Sensor(
        type=payload.type,
        location=payload.location,
        min_value=payload.min_value,
        max_value=payload.max_value
    )
    db.add(sensor)
    await db.commit()
    await db.refresh(sensor)
    return sensor


@router.post("/{sensor_id}/read", response_model=SensorReading)
async def record_reading(
    sensor_id: int, reading: SensorReading, db: AsyncSession = Depends(get_db)
):
    # Check sensor exists
    result = await db.execute(select(Sensor).filter(Sensor.id == sensor_id))
    if not result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )

    # Store reading
    db_reading = Reading(sensor_id=sensor_id, value=reading.value)

    db.add(db_reading)
    await db.commit()
    await db.refresh(db_reading)

    return db_reading


@router.get("/")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sensor))
    sensors = result.scalars().all()
    return sensors


@router.get("/{sensor_id}")
async def get_sensor(sensor_id: int, db: AsyncSession = Depends(get_db)):
    sensor = (
        await db.execute(select(Sensor).where(Sensor.id == sensor_id))
    ).scalar_one_or_none()

    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor {sensor_id} not found",
        )
    return sensor


@router.get("/{sensor_id}/readings")
async def get_sensor_readings(sensor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reading).where(Reading.sensor_id == sensor_id))
    readings = result.scalars().all()

    return readings
