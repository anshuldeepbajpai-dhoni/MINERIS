# Security Architecture

## Authentication

- JWT bearer access token with a configurable expiration
- Password hashing using bcrypt
- Public registration always creates a `viewer` account; callers cannot
  assign themselves an elevated role

## Authorization

RBAC roles:

```text
ADMIN
GEOLOGIST
MINE_PLANNER
OPERATIONS_MANAGER
DATA_ANALYST
VIEWER
```

Protected endpoints require an active authenticated user. The admin test
endpoint additionally checks the `admin` role. Role checks should be added to
other write or administrative routes as those routes are introduced.

## API Security

- HTTPS/TLS in deployment
- CORS allowlist
- Pydantic validation
- Rate limiting
- Secure HTTP headers
- Parameterized database queries/ORM
- No secrets in source code
- Environment variables for credentials
- Avoid logging token contents or credentials

## Rate Limiting

Suggested prototype limits:

```text
Authenticated normal API: 100 requests/minute
Authentication endpoints: 10 requests/minute
Heavy prediction endpoints: 10 requests/minute
```

These are initial engineering defaults, not production capacity guarantees.

## Caching

Redis may cache:
- dashboard summaries
- frequently requested mine metadata
- forecast results
- weather data

Do not cache sensitive user-specific data without an explicit cache-key strategy.

## File Upload Security

For CSV/GeoJSON/GeoTIFF uploads:

1. Authenticate user.
2. Enforce file-size limit.
3. Validate extension and MIME type.
4. Store temporarily.
5. Validate schema/content.
6. Process in a controlled worker.
7. Move accepted data to persistent storage.

## Audit Events

Audit important actions when operational logging is added:

- login
- failed login
- user/role changes
- data upload
- prediction execution
- recommendation acknowledgement
- administrative changes
