# System Architecture

## Current architecture

MINERIS is a modular monolith. The API calculates predictions and forecasts
synchronously. There is no worker process or required Redis service.

```text
React + TypeScript + Leaflet
          |
       REST/JSON
          |
FastAPI modular monolith
  |       |        |
 Auth   Mine   Intelligence
          |        |
          +--- PostgreSQL + PostGIS
                   |
          Local joblib model artifact
```

## Application layers

- **Frontend:** React, TypeScript, Leaflet, and repository CSS.
- **API:** FastAPI routers, Pydantic schemas, bearer-token authentication, and
  SQLAlchemy sessions.
- **Intelligence:** scikit-learn Random Forest inference, an annual linear-trend
  production forecast, and rule-based risk/recommendation logic.
- **Data:** PostgreSQL/PostGIS and persisted mine, production, user, and
  prospectivity records.

## Current data flow

The frontend loads authenticated mine GeoJSON and the all-mine prospectivity
overview. Selecting a mine requests its detailed prospectivity result,
production analysis, and decision support. Prospectivity results are stored
against the active model version. PostgreSQL advisory locks serialize
prediction creation across API workers.

## Limitations

Training data is synthetic and current mine feature inputs are fixed
domain-informed demo values. No live satellite, drilling, assay, or operational
feed ingestion is implemented. Docker, CI, deployed TLS, monitoring, and
background workers are not configured. Outputs are demonstration indicators,
not reserve estimates.
