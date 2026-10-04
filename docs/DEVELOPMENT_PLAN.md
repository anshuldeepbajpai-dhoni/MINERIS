# Two-Day Development Plan

The goal is a convincing, working SIH prototype — not a full production mining platform.

## DAY 1 — Foundation + Core Intelligence

### Block 1: Project Foundation
- Create repository
- Create directory structure
- Setup Python environment
- Setup React/Vite
- Setup `.env.example`
- Setup Git
- Setup Docker skeleton

### Block 2: Backend
- FastAPI application
- Configuration
- PostgreSQL connection
- Basic models
- API versioning
- Error handling
- JWT authentication
- RBAC

### Block 3: Database
Create:
- users
- roles
- mines
- drill_holes
- production_records
- equipment
- predictions
- risks
- recommendations

Seed one realistic demo mine.

### Block 4: AI Prototype
Build simple, explainable baseline models:
- prospectivity classification/demo
- production forecast
- shortfall-risk classifier

Use public/synthetic data if real mine data is unavailable.

### Block 5: Geospatial
- Mine boundary
- Drill-hole points
- Prospectivity grid/layer
- Map visualization

## DAY 2 — Dashboard + Integration + Engineering

### Block 1: Frontend
Build:
- Login
- Dashboard
- Mine selector
- GIS map
- Production panel
- Risk panel
- Recommendations panel

### Block 2: API Integration
Connect frontend to:
- auth
- mines
- map layers
- production
- predictions
- risks
- recommendations

### Block 3: Redis
Add:
- dashboard cache
- prediction-result cache
- basic rate limiting

### Block 4: Testing
At minimum:
- auth test
- RBAC test
- mine API test
- prediction API test
- recommendation API test
- frontend smoke test

### Block 5: CI/CD
GitHub Actions:
- install
- lint
- tests
- build frontend
- build backend
- security/dependency check

### Block 6: Demo Polish
Ensure this exact flow works:

```text
Login
  ↓
Select Mine
  ↓
Map
  ↓
Prospectivity
  ↓
Production Forecast
  ↓
Shortfall Risk
  ↓
Risk Explanation
  ↓
Recommendations
```

## Priority Rule

If time becomes limited:

### P0 — Must work
Authentication, dashboard, map, prediction demo, production forecast, shortfall risk, recommendations.

### P1 — Important
RBAC, PostgreSQL/PostGIS, Redis, tests, CI.

### P2 — Nice to have
Live satellite ingestion, advanced deep learning, Celery workers, Prometheus/Grafana.

Do not sacrifice the working demo to implement infrastructure that cannot be demonstrated.
