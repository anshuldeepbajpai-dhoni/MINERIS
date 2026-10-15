# Database Design

## Database

PostgreSQL with PostGIS is required for mine geometry queries. Alembic
migrations under `backend/app/db/migrations/versions` are authoritative.

## Current entities

```text
users
mines (MULTIPOLYGON, SRID 4326)
drill_holes (POINT, SRID 4326)
production_records
equipment
predictions
prospectivity_results
risks
recommendations
```

Roles are stored on `users`; separate role and permission tables do not exist.
Geological layers, assays, satellite observations, weather records, audit logs,
and model-version tables are not implemented. The current migrations do not
add GiST geometry indexes.

## Relationships

Mine records are referenced by drill holes, production records, equipment,
predictions, prospectivity results, risks, and recommendations. Mine IDs are
database-generated and must be resolved from the database.

## Demo data

The included training dataset and mine/production seeds are demonstration
data. They are not verified MOIL or other operational observations. Seed
scripts should only be used after checking the target database.
