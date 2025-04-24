# app/main.py

import asyncio
import time
from fastapi import (
    FastAPI,
    Request,
    Response
)
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.config import settings
from app.routers import actuators, sensors
from app.utils import logger
from app.utils.mqtt_client import mqtt_client
from app.background_tasks.jobs.sensor_simulator import simulate_sensors


# Create the FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    print("Starting up the application...")
    # Initialize database (create tables if they don't exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize MQTT client
    await mqtt_client.connect()
    asyncio.create_task(mqtt_client.listen())

    asyncio.create_task(simulate_sensors())  # Start sensor simulation

    try:
        yield
    finally:
        await mqtt_client.disconnect()
        print("Shutting down the application...")

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG,  # Enable debug mode if in development
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Include routers
app.include_router(sensors.router)
app.include_router(actuators.router)


# Middleware to log route endpoints
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Extract real client IP
    client_ip = request.headers.get("X-Forwarded-For") or request.headers.get("X-Real-IP") or request.client.host
    endpoint = request.url.path
    method = request.method
    
    logger.info(f"Request: {method} {endpoint} from {client_ip}")
    
    response: Response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Response: {method} {endpoint} from {client_ip} returned {response.status_code} in {duration:.2f}s"
    )
    return response



# Root endpoint for health check
@app.get("/", tags=["Health"])
def read_root():
    return {"message": f"{settings.APP_NAME} is running"}