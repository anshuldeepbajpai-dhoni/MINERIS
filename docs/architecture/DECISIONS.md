# Architecture Decisions

## ADR-001: Modular Monolith

### Decision
Use a modular FastAPI backend rather than multiple microservices for the two-day prototype.

### Reason
One developer needs rapid development, easy debugging and simple deployment.

### Future
Modules can later be extracted into services if scale requires it.

## ADR-002: PostgreSQL + PostGIS

### Decision
Use PostgreSQL with PostGIS.

### Reason
MINERIS is inherently spatial and requires geometry-aware queries.

## ADR-003: Redis

### Decision
Use Redis for caching and future background-job support.

### Reason
It provides a simple path to rate limiting, cache management and asynchronous processing.

## ADR-004: Human-in-the-Loop Recommendations

### Decision
AI produces candidate recommendations; mine personnel make the final decision.

### Reason
Operational mining decisions require domain validation and accountability.
