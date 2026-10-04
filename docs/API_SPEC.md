# API Specification

Base path:

```text
/api/v1
```

## Authentication

```http
POST /auth/login
POST /auth/refresh
POST /auth/logout
GET  /auth/me
```

## Mines

```http
GET    /mines
POST   /mines
GET    /mines/{mine_id}
PUT    /mines/{mine_id}
DELETE /mines/{mine_id}
```

## Geospatial

```http
GET /mines/{mine_id}/layers
GET /mines/{mine_id}/boundary
GET /mines/{mine_id}/prospectivity
GET /mines/{mine_id}/drill-holes
```

## Production

```http
GET /mines/{mine_id}/production
GET /mines/{mine_id}/production/forecast
GET /mines/{mine_id}/production/shortfall
```

## Equipment

```http
GET /mines/{mine_id}/equipment
GET /equipment/{equipment_id}/risk
```

## Risk

```http
GET /mines/{mine_id}/risks
GET /mines/{mine_id}/risks/summary
```

## Recommendations

```http
GET  /mines/{mine_id}/recommendations
POST /recommendations/{recommendation_id}/acknowledge
POST /recommendations/{recommendation_id}/resolve
```

## Predictions

```http
POST /predictions/prospectivity
POST /predictions/production
POST /predictions/shortfall
GET  /predictions/{prediction_id}
```

## Standard Response

```json
{
  "success": true,
  "data": {},
  "message": "Request completed",
  "request_id": "uuid"
}
```

## Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input"
  },
  "request_id": "uuid"
}
```

## API Rules

- Version APIs from day one.
- Validate request bodies.
- Use authentication for protected endpoints.
- Apply RBAC.
- Rate-limit expensive endpoints.
- Never expose stack traces to clients.
- Use request IDs for tracing.
