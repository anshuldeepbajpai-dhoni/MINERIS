# Security Architecture

## Authentication

- JWT access token
- Refresh token
- Password hashing using Argon2id or bcrypt
- Short-lived access tokens

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

Every protected endpoint checks permissions.

## API Security

- HTTPS/TLS in deployment
- CORS allowlist
- Pydantic validation
- Rate limiting
- Secure HTTP headers
- Parameterized database queries/ORM
- No secrets in source code
- Environment variables for credentials
- Audit logging

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

Record important actions:

- login
- failed login
- user/role changes
- data upload
- prediction execution
- recommendation acknowledgement
- administrative changes
