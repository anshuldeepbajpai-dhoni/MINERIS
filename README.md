# MINERIS

## Mineral Intelligence & Resource Information System

**SIH 2026 | Problem Statement 26009**

> Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.

MINERIS is a prototype decision-support platform that combines geospatial/satellite indicators, geological and drilling information, historical production, equipment conditions, and weather data to support manganese resource intelligence and production shortfall prediction.

### Core principle

**Predict → Explain → Support Decisions**

MINERIS is a decision-support system. It does not replace geological validation, mine engineering judgment, statutory processes, or formal reserve/resource estimation.

## MVP for the 2-Day Build

### Must Have
- Authentication with JWT
- Role-based access
- Mine dashboard
- Interactive map
- Sample geological/drilling data
- Mineral prospectivity prediction/demo layer
- Production forecast
- Shortfall-risk prediction
- Explainable risk factors
- Recommendations
- REST API
- PostgreSQL/PostGIS-ready data model
- Redis-ready caching/job architecture
- Basic tests
- Docker-ready setup

### Can Be Mocked/Demo-Driven
- Live satellite ingestion
- Live MOIL operational feeds
- Real-time IoT equipment telemetry
- Production-grade satellite processing
- Full 3D geological modeling
- Large-scale distributed processing

Do not claim private MOIL data or real-world accuracy unless verified.

## Repository Structure

```text
MINERIS/
├── backend/                 # FastAPI application
├── frontend/                # React + TypeScript dashboard
├── ml/                      # ML training, inference and evaluation
├── geospatial/              # GIS/satellite processing
├── database/                # Schema, migrations and seed data
├── tests/                   # Cross-module and E2E tests
├── scripts/                 # Setup/import/utility scripts
├── docs/                    # Project documentation
└── .github/workflows/       # CI/CD
```

See `docs/PROJECT_SCOPE.md` for scope and `docs/DEVELOPMENT_PLAN.md` for the 2-day execution plan.
