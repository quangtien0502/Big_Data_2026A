You are working on a Big Data course project.

PROJECT:
"Big Data Integration and Statistical Analysis System for Urban Traffic Data"

The project aims to:
- Collect traffic data from multiple heterogeneous sources.
- Clean and normalize data.
- Integrate multiple datasets.
- Process large-scale data using Apache Spark / PySpark.
- Perform statistical analysis.
- Detect simple statistical anomalies.
- Store processed data.
- Provide APIs for the frontend/dashboard.

IMPORTANT PROJECT CONSTRAINTS:
- Team size: 2 people.
- Implementation language: Python.
- Backend framework: FastAPI.
- Database: PostgreSQL.
- Big Data processing: PySpark.
- Dashboard/frontend will be implemented later.
- No AI/ML.
- No embedded programming.
- Do not introduce unnecessary infrastructure.
- Kafka is NOT required for the MVP.
- Keep the system simple enough for a university Big Data project.
- The architecture must still clearly demonstrate Big Data Integration and Processing.

The current task is ONLY PHASE 1:
BUILD THE BACKEND.

Do NOT implement the entire Big Data pipeline yet.
Do NOT implement the dashboard yet.
Do NOT introduce AI/ML.

==================================================
1. BACKEND TECHNOLOGY STACK
==================================================

Use:

- Python 3.12+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic / Pydantic Settings
- psycopg
- python-dotenv if needed
- Docker / Docker Compose for PostgreSQL

Use async FastAPI where appropriate, but do not over-engineer the project.

The backend must expose REST APIs.

==================================================
2. PROJECT ARCHITECTURE
==================================================

Create a clean layered architecture.

Recommended structure:

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── traffic.py
│   │   ├── weather.py
│   │   ├── road.py
│   │   └── processed_traffic.py
│   │
│   ├── schemas/
│   │   ├── traffic.py
│   │   ├── weather.py
│   │   ├── road.py
│   │   └── common.py
│   │
│   ├── repositories/
│   │   ├── traffic_repository.py
│   │   ├── weather_repository.py
│   │   └── road_repository.py
│   │
│   ├── services/
│   │   ├── traffic_service.py
│   │   ├── weather_service.py
│   │   └── road_service.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── health.py
│   │       ├── traffic.py
│   │       ├── weather.py
│   │       ├── road.py
│   │       └── statistics.py
│   │
│   └── utils/
│       └── ...
│
├── tests/
│   ├── test_health.py
│   ├── test_traffic.py
│   └── test_statistics.py
│
├── migrations/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

Keep modules separated by responsibility.

Do NOT put business logic directly inside FastAPI route functions.

==================================================
3. DATABASE DESIGN
==================================================

Use PostgreSQL.

At this stage create the basic database model required for the future Big Data pipeline.

TABLE 1: roads

Fields:

- id
- road_id
- road_name
- district
- latitude
- longitude
- created_at

road_id should be unique.

TABLE 2: traffic_records

Fields:

- id
- road_id
- timestamp
- vehicle_count
- avg_speed
- source
- created_at

Relationships:

traffic_records.road_id
    ->
roads.road_id

TABLE 3: weather_records

Fields:

- id
- station_id
- timestamp
- temperature
- rainfall
- weather_condition
- latitude
- longitude
- source
- created_at

TABLE 4: processed_traffic_records

This table represents data after future integration/processing.

Fields:

- id
- road_id
- timestamp
- district
- latitude
- longitude
- vehicle_count
- avg_speed
- temperature
- rainfall
- anomaly_score
- is_anomaly
- created_at

IMPORTANT:

The processed table is intentionally designed so that future PySpark jobs can generate data compatible with the backend.

Do NOT implement Spark processing yet.

==================================================
4. DATABASE MIGRATION
==================================================

Use Alembic.

Create:

- initial migration
- all required tables
- indexes

Important indexes:

traffic_records:
- timestamp
- road_id
- (road_id, timestamp)

weather_records:
- timestamp
- station_id

processed_traffic_records:
- timestamp
- road_id
- district

Do not create unnecessary indexes.

==================================================
5. CONFIGURATION
==================================================

Use environment variables.

Example:

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/traffic_bigdata

APP_NAME=Traffic Big Data Backend
DEBUG=true

Create:

.env.example

Never commit .env.

==================================================
6. DATABASE CONNECTION
==================================================

Implement a clean SQLAlchemy database layer.

Requirements:

- engine
- session factory
- dependency for FastAPI routes
- clean session management
- proper connection configuration

Do not create a global manually-managed connection inside route handlers.

==================================================
7. HEALTH CHECK API
==================================================

Create:

GET /api/v1/health

Response:

{
    "status": "ok"
}

Also create:

GET /api/v1/health/db

This endpoint verifies that the backend can connect to PostgreSQL.

Example:

{
    "status": "ok",
    "database": "connected"
}

==================================================
8. TRAFFIC API
==================================================

Create REST endpoints.

POST /api/v1/traffic

Create a traffic record.

GET /api/v1/traffic

Return traffic records.

Support:

- page
- page_size
- road_id
- start_time
- end_time

Example:

GET /api/v1/traffic?road_id=R001&start_time=...&end_time=...

GET /api/v1/traffic/{id}

GET /api/v1/traffic/road/{road_id}

Return traffic data for a specific road.

Do NOT implement complicated filtering.

==================================================
9. WEATHER API
==================================================

Create:

POST /api/v1/weather

GET /api/v1/weather

GET /api/v1/weather/{id}

GET /api/v1/weather/station/{station_id}

Support basic:

- start_time
- end_time
- station_id

==================================================
10. ROAD API
==================================================

Create:

POST /api/v1/roads

GET /api/v1/roads

GET /api/v1/roads/{road_id}

GET /api/v1/roads/{road_id}/traffic

The last endpoint should return traffic records belonging to that road.

==================================================
11. STATISTICS API
==================================================

Do NOT perform complex Big Data processing inside FastAPI.

For now, create the API contract only.

Create:

GET /api/v1/statistics/traffic

Parameters:

- start_time
- end_time
- road_id
- district
- aggregation

Supported aggregation:

- hourly
- daily
- district

Example response:

{
    "aggregation": "hourly",
    "data": [
        {
            "time": "...",
            "avg_vehicle_count": 123.4,
            "avg_speed": 35.2
        }
    ]
}

For this first phase, the implementation may use PostgreSQL aggregation.

Later, replace/extend the processing layer with PySpark.

==================================================
12. ANOMALY API
==================================================

Create API contract:

GET /api/v1/statistics/anomalies

Parameters:

- start_time
- end_time
- road_id
- district

Return:

{
    "data": [
        {
            "road_id": "R001",
            "timestamp": "...",
            "vehicle_count": 500,
            "is_anomaly": true,
            "anomaly_score": 3.42
        }
    ]
}

For now, do not implement ML.

The future implementation will use statistical methods such as:

Z-score:

z = (x - mean) / standard_deviation

Potential anomaly:

abs(z) > 3

But do not over-engineer this phase.

==================================================
13. DATA IMPORT API
==================================================

Create a simple endpoint for importing CSV data.

POST /api/v1/import/traffic

POST /api/v1/import/weather

POST /api/v1/import/roads

The endpoint should accept CSV files.

Basic workflow:

CSV
 ↓
Validate columns
 ↓
Parse records
 ↓
Validate data types
 ↓
Insert into PostgreSQL

The import layer must be separated from the future PySpark pipeline.

IMPORTANT:

This is only a simple import mechanism for development/testing.

Large-scale processing will later be handled by PySpark.

==================================================
14. VALIDATION
==================================================

Use Pydantic.

Validate:

Traffic:

- road_id required
- timestamp required
- vehicle_count >= 0
- avg_speed >= 0

Weather:

- station_id required
- timestamp required
- rainfall >= 0

Road:

- road_id required
- latitude between -90 and 90
- longitude between -180 and 180

Return proper HTTP errors.

==================================================
15. ERROR HANDLING
==================================================

Implement consistent API errors.

Example:

{
    "detail": "Road R001 not found"
}

Handle:

- validation errors
- duplicate road_id
- missing records
- database errors

Do not expose internal database errors to API clients.

==================================================
16. PAGINATION
==================================================

For list endpoints:

page = 1
page_size = 20

Response:

{
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 100
}

Implement reusable pagination logic if practical.

==================================================
17. API DOCUMENTATION
==================================================

FastAPI should automatically expose:

/docs

/redoc

Make sure every endpoint has:

- summary
- description
- request schema
- response schema
- status codes

==================================================
18. DOCKER
==================================================

Create docker-compose.yml.

At minimum:

services:

  postgres

Do NOT add Spark containers yet.

Do NOT add Kafka.

Do NOT add Redis.

Do NOT add unnecessary services.

The backend can initially run locally with:

uvicorn app.main:app --reload

PostgreSQL runs through Docker.

==================================================
19. TESTING
==================================================

Create basic pytest tests.

Minimum:

- health endpoint
- database connection
- create road
- get road
- create traffic record
- get traffic records
- traffic filtering
- statistics endpoint

Do not aim for 100% coverage.

Focus on core business functionality.

==================================================
20. README
==================================================

Create a README explaining:

1. Project overview
2. Technology stack
3. Architecture
4. Folder structure
5. Database schema
6. Environment variables
7. How to start PostgreSQL
8. How to install Python dependencies
9. How to run migrations
10. How to start FastAPI
11. API documentation
12. Running tests
13. Future integration with PySpark

Include an architecture diagram using Mermaid if possible.

Architecture:

Data Sources
     |
     v
Python Data Import
     |
     v
PostgreSQL
     |
     v
FastAPI
     |
     v
Dashboard

Future:

Data Sources
     |
     v
Raw Data
     |
     v
PySpark
     |
     +--> Cleaning
     |
     +--> Schema Mapping
     |
     +--> Data Integration
     |
     +--> Statistical Analysis
     |
     +--> Anomaly Detection
     |
     v
Processed Data
     |
     v
PostgreSQL
     |
     v
FastAPI
     |
     v
Dashboard

==================================================
21. DEVELOPMENT PRINCIPLES
==================================================

Follow these principles:

1. Keep the code simple.
2. Do not over-engineer.
3. Separate API, service, repository and database layers.
4. Use type hints.
5. Use Pydantic models.
6. Use SQLAlchemy ORM.
7. Use Alembic migrations.
8. Use environment variables.
9. Write clear README documentation.
10. Keep future PySpark integration in mind.
11. Do not introduce AI/ML.
12. Do not introduce Kafka.
13. Do not introduce microservices.
14. Do not introduce Kubernetes.
15. Do not introduce authentication unless necessary.
16. Do not implement the frontend yet.

==================================================
22. EXPECTED RESULT
==================================================

At the end of this task, the following must work:

1. PostgreSQL starts with Docker.

2. Alembic creates the database tables.

3. FastAPI starts successfully.

4. Swagger is available at:

/docs

5. Health check works.

6. Roads can be created/read.

7. Traffic records can be created/read.

8. Weather records can be created/read.

9. CSV data can be imported.

10. Basic traffic statistics API works.

11. Tests pass.

12. README explains how to run everything.

13. Project structure is ready for the next phase:
   PySpark Data Processing & Big Data Integration.

==================================================
23. IMPORTANT IMPLEMENTATION ORDER
==================================================

Do the work in this exact order:

STEP 1
Initialize Python project.

STEP 2
Create folder structure.

STEP 3
Configure FastAPI.

STEP 4
Configure PostgreSQL.

STEP 5
Configure SQLAlchemy.

STEP 6
Configure Alembic.

STEP 7
Create database models.

STEP 8
Create migrations.

STEP 9
Create Pydantic schemas.

STEP 10
Create repositories.

STEP 11
Create services.

STEP 12
Create API routes.

STEP 13
Create CSV import.

STEP 14
Create statistics API.

STEP 15
Add validation and error handling.

STEP 16
Add tests.

STEP 17
Add Docker configuration.

STEP 18
Write README.

STEP 19
Run the entire system and verify all endpoints.

Do not move to PySpark until this phase is working.

==================================================
FINAL REQUIREMENT
==================================================

Before finishing, provide:

1. Complete project tree.
2. List of implemented APIs.
3. Database ERD or Mermaid ER diagram.
4. How to run the project.
5. Example API requests.
6. Test results.
7. List of TODO items for the next PySpark phase.

Do not claim that something works unless it has actually been tested.