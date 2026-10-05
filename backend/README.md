# Big Data Integration and Statistical Analysis System - Backend

This is the backend component for the "Big Data Integration and Statistical Analysis System for Urban Traffic Data" project. It provides basic web APIs to create, read, and manage road, traffic, and weather data. The backend is built using FastAPI, PostgreSQL, SQLAlchemy, and Alembic.

## Technology Stack

- **Python**: 3.12+
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Docker)
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic
- **Validation**: Pydantic v2

## Folder Structure

```text
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core config & database connection
│   ├── models/       # SQLAlchemy database models
│   ├── repositories/ # Database interaction layer (CRUD)
│   ├── schemas/      # Pydantic validation schemas
│   ├── services/     # Business logic
│   └── main.py       # FastAPI application entrypoint
├── migrations/       # Alembic migrations directory
├── tests/            # Pytest test cases
├── docker-compose.yml# PostgreSQL Docker compose setup
├── requirements.txt  # Python dependencies
└── .env.example      # Environment variables template
```

## Database Schema (ERD Overview)

- **roads**: Contains information about roads (`road_id`, `road_name`, `district`, `latitude`, `longitude`).
- **traffic_records**: Traffic counts linked to a road via `road_id`.
- **weather_records**: Environmental data associated with a `station_id`.
- **processed_traffic_records**: Designed to store processed anomaly data resulting from future PySpark batch/stream integration.

## Getting Started

### 1. Start PostgreSQL
Make sure you have Docker installed.

```bash
cd backend
docker-compose up -d
```

### 2. Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Ensure the `DATABASE_URL` matches your local setup.

### 3. Install Python Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Migrations
Generate database tables by running Alembic:
```bash
alembic upgrade head
```

### 5. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, the interactive API documentation (Swagger UI) is available at:

- **Swagger**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example Requests

**Check Database Health**
```bash
curl http://localhost:8000/api/v1/health/db
```

**Create a Road**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/roads/' \
  -H 'Content-Type: application/json' \
  -d '{
  "road_id": "R001",
  "road_name": "Main Street",
  "district": "Downtown",
  "latitude": 21.0,
  "longitude": 105.8
}'
```

**Create a Traffic Record**
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/traffic/' \
  -H 'Content-Type: application/json' \
  -d '{
  "road_id": "R001",
  "timestamp": "2023-10-01T10:00:00Z",
  "vehicle_count": 120,
  "avg_speed": 40.5,
  "source": "sensor-1"
}'
```

## Running Tests

Tests use an in-memory SQLite database, making them fast and isolated. Run pytest:
```bash
pytest tests/
```

## Next Phase: PySpark Integration

- **Data Importer**: Create CSV ingest endpoints mapping static sets into PostgreSQL.
- **Big Data Jobs**: PySpark jobs to process raw traffic data and load it into `processed_traffic_records` table with anomaly tagging.
- **Statistics Implementation**: Add logic inside `api/routes/statistics.py` to aggregate counts and display anomaly charts.
