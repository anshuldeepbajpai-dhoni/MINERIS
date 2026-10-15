# Project Scope

This document describes the intended domain and separates it from the current
prototype. The current implementation uses demo inputs; future capabilities
below should not be presented as already integrated.

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
- JWT access tokens (no refresh-token endpoint)
- Password hashing
- Role checks; public registration creates viewer accounts

### B. Mine Intelligence
- Mine list
- Mine details
- Mine boundary
- Mine GeoJSON boundaries
- Drill-hole model exists; no dashboard API is currently exposed

### C. Geospatial Intelligence
- Map visualization
- All-mine prospectivity classifications on the map
- Per-mine score, confidence, class probabilities, and feature importance
- Current inputs are synthetic/demo values, not live satellite data

### D. Production Intelligence
- Historical production
- Target vs actual
- Forecast
- Shortfall risk

### E. Operational Risk
- Equipment model exists; no current equipment-risk API integration

### F. Recommendation Engine
- Identify major risk drivers
- Generate candidate corrective actions
- Allow human review/acknowledgement

## 4. Non-Functional Scope

- Secure authentication
- API validation
- Focused backend unit tests
- Local development configuration

Rate limiting, caching, CI, containerized deployment, and monitoring are not
currently implemented.

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
