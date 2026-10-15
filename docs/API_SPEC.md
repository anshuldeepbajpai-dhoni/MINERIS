# API Specification

Base path: `/api/v1`

Interactive OpenAPI documentation is available at `/docs` when the backend is
running.

## Authentication

| Method | Path | Access | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/register` | Public | Create an account with the `viewer` role |
| POST | `/auth/login` | Public | Exchange form-encoded username/password for a bearer token |
| GET | `/auth/me` | Bearer token | Return the current active user |
| GET | `/auth/admin-test` | Admin | Verify the admin role check |

There is no refresh-token endpoint. Access-token expiry is configured with
`ACCESS_TOKEN_EXPIRE_MINUTES`; sign in again after expiry. Registration ignores
caller-supplied roles and always creates a viewer account.

## Mines and geospatial data

| Method | Path | Access | Purpose |
| --- | --- | --- | --- |
| GET | `/mines` | Bearer token | List mines |
| GET | `/mines/{mine_id}` | Bearer token | Retrieve one mine |
| GET | `/mines/geojson` | Bearer token | Return all mine boundaries as a GeoJSON FeatureCollection |
| GET | `/mines/{mine_id}/prospectivity` | Bearer token | Retrieve or create a mine prediction |
| GET | `/mines/prospectivity-overview` | Bearer token | Return one active-model result per mine |

The overview entries contain `mine_id`, `mine_name`, `score` (0–100),
`classification`, `confidence`, and `model_version`. An empty mine table
returns an empty array. A missing or unreadable model artifact returns HTTP 503.

## Production and decision support

| Method | Path | Access | Purpose |
| --- | --- | --- | --- |
| GET | `/mines/{mine_id}/production` | Bearer token | Historical production, trend forecast, shortfall, and risk |
| GET | `/mines/{mine_id}/decision-support` | Bearer token | Prospectivity summary and production recommendations |

Production returns HTTP 404 when a mine has no production records. Decision
support returns an explicit `production_available: false` response when
production history is missing.

## Health

`GET /health` returns the API health status. `GET /` returns basic service
metadata. These endpoints do not check database connectivity.

Protected endpoints require `Authorization: Bearer <access_token>`. Errors use
FastAPI's standard JSON error format; endpoint-specific status codes and
schemas are visible in the generated OpenAPI document.
