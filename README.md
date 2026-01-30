# Smart Farm API

Backend infrastructure for IoT-based agricultural monitoring. Handles device registration, MQTT communication, sensor data logging, and command execution.

## What it does

- Registers and manages IoT devices (sensors, actuators)
- Receives sensor data over MQTT and stores it
- Sends commands to actuators with full audit trails
- Provides a REST API for dashboards and integrations

```
[ESP32/Arduino] → MQTT → [This API] → [PostgreSQL]
                              ↓
                    REST endpoints for your app
```

## Setup

**Requirements:** Python 3.8+, Eclipse Mosquitto

```bash
git clone https://github.com/Incognitol07/smart-farm-api
cd smart-farm-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Initialize database
alembic upgrade head

# Start MQTT broker (separate terminal)
mosquitto -c mosquitto/config/mosquitto.conf

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs at `http://localhost:8000/docs`

## MQTT Topics

Your hardware publishes/subscribes to:

| Topic                 | Direction    | Purpose         |
| --------------------- | ------------ | --------------- |
| `farm/sensors/{id}`   | Device → API | Sensor readings |
| `farm/actuators/{id}` | API → Device | Commands        |

The API handles storage, logging, and serving data to frontends. Your microcontroller handles the actual sensor reading and actuator control.

## Project Structure

```
app/
├── main.py          # FastAPI entry point
├── models/          # SQLAlchemy models
├── routers/         # API endpoints
├── services/        # Business logic + MQTT
└── schemas/         # Pydantic models
mosquitto/           # MQTT broker config
alembic/             # Database migrations
```

## Contributing

Open an issue first if you're planning something big. PRs welcome for bug fixes and improvements.

## License

MIT
