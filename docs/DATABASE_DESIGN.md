# Database Design

## Primary Database

**PostgreSQL + PostGIS**

PostGIS is required for mine boundaries, drill-hole coordinates, geological polygons and spatial queries.

## Core Entities

```text
users
roles
permissions
user_roles

mines
mine_boundaries

geological_layers
geological_features

drill_holes
assay_results

satellite_observations

production_records
production_targets

equipment
equipment_events
maintenance_records

weather_records

predictions
prediction_features
model_versions

risk_events
recommendations

audit_logs
```

## Key Relationships

```text
Mine
 |
 +-- Mine Boundary
 +-- Geological Layers
 +-- Drill Holes
 |     +-- Assay Results
 +-- Production Records
 +-- Equipment
 |     +-- Equipment Events
 +-- Weather Records
 +-- Predictions
 +-- Risks
 +-- Recommendations
```

## Spatial Data

Use PostGIS geometry types:

- `POINT` — drill holes, equipment locations
- `LINESTRING` — roads/haul routes if available
- `POLYGON/MULTIPOLYGON` — mine boundaries, geological zones, risk zones

Use GiST spatial indexes for frequently queried geometry columns.

## Important Indexes

- `users.email`
- `production_records.mine_id, date`
- `equipment.mine_id`
- `predictions.mine_id, created_at`
- spatial GiST indexes on geometry columns

## Prototype Data

For the two-day build, use clearly labelled synthetic/public sample data where real operational data is unavailable.

Never label synthetic data as MOIL operational data.
