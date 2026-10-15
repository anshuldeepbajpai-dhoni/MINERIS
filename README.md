# MINERIS

## Mineral Intelligence & Resource Information System

**SIH 2026 | Problem Statement 26009**

> Using AI/ML and Space Technology to Identify Manganese Reserves and Overcome Production Shortfalls.

MINERIS is a prototype decision-support platform that combines geospatial/satellite indicators, geological and drilling information, historical production, equipment conditions, and weather data to support manganese resource intelligence and production shortfall prediction.

### Core principle

**Predict → Explain → Support Decisions**

MINERIS is a decision-support system. It does not replace geological validation, mine engineering judgment, statutory processes, or formal reserve/resource estimation.

## MVP for the 2-Day Build

### Must Have
- Authentication with JWT
- Role-based access
- Mine dashboard
- Interactive map
- Sample geological/drilling data
- Mineral prospectivity prediction/demo layer
- Production forecast
- Shortfall-risk prediction
- Explainable risk factors
- Recommendations
- REST API
- PostgreSQL/PostGIS-ready data model
- Redis-ready caching/job architecture
- Basic tests
- Docker-ready setup

### Can Be Mocked/Demo-Driven
- Live satellite ingestion
- Live MOIL operational feeds
- Real-time IoT equipment telemetry
- Production-grade satellite processing
- Full 3D geological modeling
- Large-scale distributed processing

Do not claim private MOIL data or real-world accuracy unless verified.

## Repository Structure

```text
MINERIS/
├── backend/                 # FastAPI application
├── frontend/                # React + TypeScript dashboard
├── ml/                      # ML training, inference and evaluation
├── geospatial/              # GIS/satellite processing
├── database/                # Schema, migrations and seed data
├── tests/                   # Cross-module and E2E tests
├── scripts/                 # Setup/import/utility scripts
├── docs/                    # Project documentation
└── .github/workflows/       # CI/CD
```

See `docs/PROJECT_SCOPE.md` for scope and `docs/DEVELOPMENT_PLAN.md` for the 2-day execution plan.

## Current implementation

The repository is a React + TypeScript + Leaflet frontend and a FastAPI
modular-monolith backend. PostgreSQL/PostGIS stores mines, production records,
users, and persisted prospectivity results. The prospectivity classifier is a
scikit-learn Random Forest. Production forecasts use a simple historical trend.
The current dashboard supports login, mine selection, GeoJSON mapping,
per-mine prospectivity, production analysis, and decision support.

The training dataset is generated and synthetic. Current mine feature inputs
are domain-informed demo values rather than measured satellite, assay, or
drilling observations. Forecasts and risk labels are demonstration logic, not
validated operational predictions or reserve estimates.

## Windows development setup

Prerequisites: Python 3.11, Node.js with npm, and PostgreSQL with the PostGIS
extension available. Redis, Docker, and live satellite credentials are not
required by the current demo.

### Backend

From the repository root in PowerShell:

```powershell
py -3.11 -m venv backend\.venv
backend\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
```

Edit `backend\.env` with the local database URL and a unique secret. Generate
a secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Create the database, enable PostGIS (`CREATE EXTENSION postgis;`), then apply
migrations and seed demo data:

```powershell
Set-Location backend
alembic upgrade head
python scripts\seed_mines.py
python scripts\seed_production.py
uvicorn app.main:app --reload
```

The mine seed skips existing names and the production seed skips existing
mine/year records. Both scripts only add demo rows; inspect the database before
using them with non-demo data.

To regenerate the synthetic training inputs and model artifact, run from the
repository root with the backend virtual environment active:

```powershell
python -m ml.prospectivity.dataset
python -m ml.prospectivity.train
```

The checked-in development artifact is at
`ml/prospectivity/artifacts/prospectivity_rf.joblib`.

### Frontend

In another PowerShell window:

```powershell
Set-Location frontend
npm ci
npm run dev
```

Open the Vite URL printed by the command. The current API client targets
`http://127.0.0.1:8000/api/v1`; update `frontend/src/lib/api.ts` if the backend
host or port changes. Configure `CORS_ORIGINS` in `backend\.env` for the exact
frontend origin, using comma-separated origins when needed.

Public registration creates viewer accounts. There is no default admin
credential or built-in admin bootstrap flow. Do not add a production password
to the frontend or example configuration.

### API, tests, and build

With the backend virtual environment active and current directory set to
`backend`:

```powershell
python -m pytest
python -m compileall -q app tests
```

Open `http://127.0.0.1:8000/docs` for the generated OpenAPI docs. In the
frontend directory, run `npm run build` for TypeScript and production-build
validation.

## Troubleshooting

- **`ModuleNotFoundError: ml`**: start FastAPI from the `backend` directory
  with `uvicorn app.main:app --reload`. `app.main` adds the repository root so
  the existing root-level `ml` package can be imported.
- **Database connection failure**: verify PostgreSQL is running, the database
  exists, and `DATABASE_URL` in `backend\.env` uses the installed driver.
- **PostGIS function/type errors**: install PostGIS for the PostgreSQL server
  and run `CREATE EXTENSION postgis;` in the MINERIS database before migration.
- **Missing or corrupt model artifact**: regenerate it with the two ML commands
  above; the all-mine endpoint responds with HTTP 503 if inference cannot load
  the artifact.
- **Authentication failure**: register an account, sign in with its email and
  password, and confirm the browser has the `mineris_token` entry. Tokens
  expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.
- **Frontend cannot reach API**: verify the API URL in `frontend/src/lib/api.ts`,
  backend port, and the browser origin in `CORS_ORIGINS`.
- **TypeScript build error**: run `npm ci` in `frontend`, then `npm run build`
  and address the first reported TypeScript diagnostic.

## Known limitations

- No live satellite ingestion, validated reserve estimation, or operational
  MOIL feed is implemented.
- The model was trained on generated synthetic data; its accuracy is not a
  measure of real-world manganese prospectivity.
- Forecasting is a simple linear trend over annual records and does not account
  for seasonality, capacity constraints, or uncertainty intervals.
- There is no refresh-token endpoint, role-management UI, default administrator,
  Redis worker, Docker deployment, or CI workflow in the current repository.
- Database-backed end-to-end behavior requires a configured PostgreSQL/PostGIS
  service; the focused unit tests use fakes and do not validate that service.
