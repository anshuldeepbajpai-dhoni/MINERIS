# System Architecture

## Architectural Style

MINERIS uses a **modular monolith + asynchronous worker architecture** for the prototype.

This is intentionally simpler than a microservice architecture because the initial implementation is being built by one developer in two days.

```text
Users
  |
 HTTPS
  v
React + TypeScript
  |
 REST/JSON
  v
FastAPI
  |
  +-- Auth/RBAC
  +-- Mine Module
  +-- Geospatial Module
  +-- Production Module
  +-- Prediction Module
  +-- Risk Module
  +-- Recommendation Module
  |
  +-------- PostgreSQL + PostGIS
  |
  +-------- Redis
              |
              +-- Background jobs
              +-- Cache
              |
              v
         ML/Geo Workers
```

## Layers

### 1. Presentation Layer
React, TypeScript, Tailwind CSS and map visualization.

### 2. API/Application Layer
FastAPI handles:
- authentication
- authorization
- validation
- routing
- business logic
- API responses

### 3. Intelligence Layer
- Prospectivity model
- Production forecasting model
- Shortfall-risk model
- Equipment-risk logic
- Explainability
- Recommendation engine

### 4. Data Layer
- PostgreSQL
- PostGIS
- Redis
- Object storage for large raster/model artifacts

### 5. Platform Layer
- Docker
- GitHub Actions
- Nginx
- Prometheus/Grafana-ready monitoring

## Data Flow

```text
Satellite / GIS / Geological / Operational Data
                     |
                     v
              Ingestion Layer
                     |
                     v
            Feature Engineering
                     |
          +----------+----------+
          |                     |
          v                     v
   Prospectivity Model    Production/Risk Models
          |                     |
          +----------+----------+
                     v
              Risk Fusion
                     |
                     v
           Recommendation Engine
                     |
                     v
                FastAPI
                     |
                     v
             React Dashboard
```

## Important Design Constraint

Satellite data should be presented as evidence for **surface/environmental indicators and prospectivity**, not as a standalone method for certifying underground reserves. Drilling, geological and assay evidence provide subsurface validation.
