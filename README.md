# Smart Farm API

**The plug-and-play IoT infrastructure that agricultural automation companies charge $50,000+ to develop.**

## Why This Matters

Stop reinventing the wheel. Every smart farming project needs the same core infrastructure:

- Device registration and management
- Real-time MQTT communication  
- Data logging and historical tracking
- Command execution and audit trails
- Scalable monitoring dashboard

**We built it once, so you don't have to.** Deploy your microcontroller business logic, connect to our API, and focus on what makes your farm unique—not rebuilding database schemas and MQTT brokers.

## Perfect For

✅ **Agricultural Consultants** - Deploy client solutions in days, not months  
✅ **Smart Greenhouse Operators** - Professional IoT management without the development cost  
✅ **Equipment Manufacturers** - Add IoT capabilities to existing hardware  
✅ **Farm Automation Startups** - Skip the infrastructure, build the innovation  
✅ **Research Institutions** - Standardized platform for agricultural IoT experiments  

## Value Proposition

| Commercial IoT Platforms | Smart Farm API |
|-------------------------|----------------|
| $50-500/month per farm | **FREE** |
| Vendor lock-in | **Open source** |
| Limited customization | **Full control** |
| 6-month implementation | **Deploy in days** |

## Quick Start

### Prerequisites

- Python 3.8+
- Eclipse Mosquitto MQTT Broker

### Setup

```bash
# Clone and setup
git clone https://github.com/Incognitol07/smart-farm-api
cd smart-farm-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Initialize database
alembic upgrade head

# Start MQTT broker (in separate terminal)
mosquitto -c mosquitto/config/mosquitto.conf

# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**That's it!** Visit `http://localhost:8000/docs` for the documentation.

## What You Get

### Complete IoT Infrastructure

- **RESTful API** for device management and monitoring
- **MQTT communication hub** compatible with any IoT hardware  
- **Database logging** with full audit trails
- **Real-time interaction** via auto-generated Swagger UI
- **Background simulation** for immediate testing without hardware

### Perfect Architecture

```text
[Your ESP32/Arduino] → [MQTT] → [Smart Farm API] → [Database + Dashboard]
     ↑                                  ↑
Business Logic               Universal Infrastructure
(Your custom code)         (Our battle-tested platform)
```

### Ready for Hardware

Your microcontrollers just need to:

- Send sensor data to `farm/sensors/{id}`
- Listen for commands on `farm/actuators/{id}`
- Handle automation logic locally (edge computing)

The API handles everything else: storage, monitoring, scaling, and management.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue in the GitHub repository.
