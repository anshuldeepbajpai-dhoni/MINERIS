# Project Scope

## 1. Problem

Manganese reserve identification and production planning can depend on fragmented geological, operational and environmental information. The proposed system provides a unified AI/geospatial decision-support layer.

## 2. Target Users

- **Admin** — manages users, mines and system configuration.
- **Geologist** — reviews geological layers, drilling, assays and prospectivity.
- **Mine Planner** — reviews production forecasts, shortfall risks and recommendations.
- **Operations Manager** — monitors production, equipment and operational risks.
- **Analyst** — reviews analytics and reports.
- **Viewer** — read-only access.

## 3. Functional Scope

### A. Authentication
- Login
- JWT access/refresh tokens
- Password hashing
- RBAC

### B. Mine Intelligence
- Mine list
- Mine details
- Mine boundary
- Geological layers
- Drill-hole locations
- Assay/sample information

### C. Geospatial Intelligence
- Map visualization
- Satellite-derived indicators
- Prospectivity probability layer
- Confidence layer
- Spatial filtering

### D. Production Intelligence
- Historical production
- Target vs actual
- Forecast
- Shortfall risk

### E. Operational Risk
- Equipment status
- Downtime indicators
- Weather impact
- Blasting/maintenance delay indicators

### F. Recommendation Engine
- Identify major risk drivers
- Generate candidate corrective actions
- Allow human review/acknowledgement

## 4. Non-Functional Scope

- Secure authentication
- API validation
- Rate limiting
- Caching
- Structured logging
- Automated tests
- CI pipeline
- Containerized development
- Monitoring-ready architecture

## 5. Explicit Non-Goals for the 2-Day Prototype

- Certified geological reserve estimation
- Autonomous mine control
- Guaranteed underground ore detection from satellite imagery alone
- Real-time industrial equipment control
- Production deployment on MOIL infrastructure
- Large-scale distributed satellite processing

## 6. Demo Success Criteria

A judge should be able to:

1. Log in.
2. Select a mine.
3. View the mine on a map.
4. Inspect prospectivity information.
5. View production forecast.
6. See shortfall risk.
7. Understand the main contributing factors.
8. See recommended actions.
9. Understand how the platform can integrate real operational data later.
