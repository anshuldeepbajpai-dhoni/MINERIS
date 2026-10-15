# MINERIS Demo Script

## 1. Sign in

Register an account through `POST /api/v1/auth/register`, then sign in through
the dashboard. Public registration creates a viewer account. No default admin
credentials are shipped.

## 2. Select a mining zone

Use the selector or click a mine on the map. Confirm that the selected boundary
is highlighted and that the prospectivity, production, and decision panels
update for the same mine.

## 3. Review prospectivity

Show how each mine's map color reflects its own LOW, MEDIUM, or HIGH
classification. Open a popup to view its score and confidence; use the panel to
review class probabilities, feature importance, and the explanation.

The current model was trained on synthetic generated data, and current mine
feature inputs are demonstration values. Do not describe its output as
real-world accuracy or a certified reserve estimate.

## 4. Review production and recommendations

Show the available annual production history, trend forecast, demand gap, risk
classification, and decision-support recommendations. The forecast is a
simple linear trend; the current demo does not model equipment downtime,
rainfall, or blasting delays.

## 5. Close

Explain that MINERIS is a decision-support prototype. Real operational use
requires verified geological, satellite, drilling, assay, and production data
plus domain validation.
