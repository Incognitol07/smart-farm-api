# app/routers/actuators.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.config import settings
from app.utils.mqtt_client import mqtt_client
from app.config import settings
from app.models import Actuator, Command
from app.schemas.actuator import ActuatorCommand, ActuatorCreate
from app.models.actuator import ActuatorState

router = APIRouter(prefix="/actuators", tags=["actuators"])

@router.post("/")
async def create_actuator( payload: ActuatorCreate, db: AsyncSession = Depends(get_db)):
    actuator = Actuator(name=payload.name, state=payload.state)
    db.add(actuator)
    await db.commit()
    await db.refresh(actuator)
    return actuator

@router.get("/")
async def get_actuators(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actuator))
    actuators = result.scalars().all()
    return actuators

@router.get("/{actuator_id}")
async def get_actuator(actuator_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Actuator).where(Actuator.id == actuator_id))
    actuator = result.scalars().first()
    if not actuator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actuator not found")
    return actuator

@router.get("/{actuator_id}/commands")
async def get_commands(actuator_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Command).where(Command.actuator_id == actuator_id))
    commands = result.scalars().all()
    
    return commands

@router.get("/{actuator_id}/commands/{command_id}")
async def get_command(actuator_id: int, command_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Command).where(Command.actuator_id == actuator_id, Command.id == command_id))
    command = result.scalars().first()
    if not command:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Command not found")
    return command

# app/routers/actuators.py
@router.post("/command", response_model=ActuatorCommand)
async def command_actuator(
    cmd: ActuatorCommand, 
    db: AsyncSession = Depends(get_db)
):
    # Validate actuator exists
    result = await db.execute(select(Actuator).where(Actuator.id == cmd.actuator_id))
    actuator = result.scalars().first()
    if not actuator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actuator not found")

    # Create command record
    db_command = Command(
        actuator_id=cmd.actuator_id,
        command=cmd.command,
        executed=False
    )
    db.add(db_command)
    
    # Update actuator state
    actuator.state = cmd.command
    db.add(actuator)
    
    await db.commit()
    await db.refresh(db_command)

    # Publish via MQTT
    topic = f"{settings.MQTT_TOPIC_ACTUATORS}/{cmd.actuator_id}"
    await mqtt_client.publish(topic, {
        "command": cmd.command.value,
        "db_command_id": db_command.id
    })
    
    return db_command