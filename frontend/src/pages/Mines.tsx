import { useEffect, useState } from "react";

import MineMap from "../components/map/MineMap";
import ProspectivityPanel from "../components/prospectivity/ProspectivityPanel";
import ProductionPanel from "../components/production/ProductionPanel";
import DecisionSupportPanel from "../components/decision/DecisionSupportPanel";

import { apiRequest } from "../lib/api";

import type {
  MineGeoJSON,
} from "../types/mine";
import type { ProspectivityResult } from "../types/prospectivity";

import type { ProductionAnalysis } from "../types/production";
import type { DecisionSupport } from "../types/decisionSupport";

import "../styles/mines.css";

export default function Mines() {
  const [data, setData] = useState<MineGeoJSON | null>(null);

  const [selectedMineId, setSelectedMineId] =
    useState<number | null>(null);

  const [prospectivity, setProspectivity] =
    useState<ProspectivityResult | null>(null);

  const [production, setProduction] =
    useState<ProductionAnalysis | null>(null);

  const [decisionSupport, setDecisionSupport] =
    useState<DecisionSupport | null>(null);

  const [loadingMines, setLoadingMines] =
    useState(true);

  const [loadingProspectivity, setLoadingProspectivity] =
    useState(false);

  const [loadingProduction, setLoadingProduction] =
    useState(false);

  const [loadingDecisionSupport, setLoadingDecisionSupport] =
    useState(false);

  const [error, setError] = useState("");

  const [prospectivityError, setProspectivityError] =
    useState("");

  const [productionError, setProductionError] =
    useState("");

  const [decisionSupportError, setDecisionSupportError] =
    useState("");

  // --------------------------------------------------
  // LOAD MINES
  // --------------------------------------------------

  useEffect(() => {
    async function loadMines() {
      try {
        const result =
          await apiRequest<MineGeoJSON>(
            "/mines/geojson"
          );

        setData(result);

        if (result.features.length > 0) {
          setSelectedMineId(
            result.features[0].properties.id
          );
        }
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load mines"
        );
      } finally {
        setLoadingMines(false);
      }
    }

    loadMines();
  }, []);

  // --------------------------------------------------
  // LOAD PROSPECTIVITY
  // --------------------------------------------------

  useEffect(() => {
    async function loadProspectivity() {
      if (!selectedMineId) return;

      setLoadingProspectivity(true);
      setProspectivityError("");
      setProspectivity(null);

      try {
        const result =
          await apiRequest<ProspectivityResult>(
            `/mines/${selectedMineId}/prospectivity`
          );

        setProspectivity(result);
      } catch (err) {
        setProspectivityError(
          err instanceof Error
            ? err.message
            : "Failed to load prospectivity"
        );
      } finally {
        setLoadingProspectivity(false);
      }
    }

    loadProspectivity();
  }, [selectedMineId]);

  // --------------------------------------------------
  // LOAD PRODUCTION
  // --------------------------------------------------

  useEffect(() => {
    async function loadProduction() {
      if (!selectedMineId) return;

      setLoadingProduction(true);
      setProductionError("");
      setProduction(null);

      try {
        const result =
          await apiRequest<ProductionAnalysis>(
            `/mines/${selectedMineId}/production`
          );

        setProduction(result);
      } catch (err) {
        setProductionError(
          err instanceof Error
            ? err.message
            : "Failed to load production analysis"
        );
      } finally {
        setLoadingProduction(false);
      }
    }

    loadProduction();
  }, [selectedMineId]);

  // --------------------------------------------------
  // LOAD DECISION SUPPORT
  // --------------------------------------------------

  useEffect(() => {
    async function loadDecisionSupport() {
      if (!selectedMineId) return;

      setLoadingDecisionSupport(true);
      setDecisionSupportError("");
      setDecisionSupport(null);

      try {
        const result =
          await apiRequest<DecisionSupport>(
            `/mines/${selectedMineId}/decision-support`
          );

        setDecisionSupport(result);
      } catch (err) {
        setDecisionSupportError(
          err instanceof Error
            ? err.message
            : "Failed to load decision support"
        );
      } finally {
        setLoadingDecisionSupport(false);
      }
    }

    loadDecisionSupport();
  }, [selectedMineId]);

  // --------------------------------------------------
  // LOADING
  // --------------------------------------------------

  if (loadingMines) {
    return (
      <div className="mineris-loading">
        <div className="loading-spinner" />
        <h2>Loading MINERIS</h2>
        <p>
          Initializing mineral intelligence system...
        </p>
      </div>
    );
  }

  // --------------------------------------------------
  // ERROR
  // --------------------------------------------------

  if (error) {
    return (
      <div className="mineris-error">
        <h2>MINERIS System Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="mineris-error">
        <h2>No Mine Data</h2>
        <p>
          No mining zones are currently available.
        </p>
      </div>
    );
  }

  const selectedMine = data.features.find(
    (feature) =>
      feature.properties.id === selectedMineId
  );

  return (
    <div className="mineris-dashboard">

      {/* =================================================
          HEADER
      ================================================= */}

      <header className="mineris-header">

        <div className="header-brand">

          <div className="brand-icon">
            M
          </div>

          <div>
            <h1>MINERIS</h1>

            <p>
              Mineral Intelligence & Resource
              Information System
            </p>
          </div>

        </div>

        <div className="header-status">

          <span className="status-dot" />

          <span>
            SYSTEM OPERATIONAL
          </span>

        </div>

      </header>


      {/* =================================================
          MINE SELECTOR
      ================================================= */}

      <section className="mine-selector-section">

        <div>

          <div className="section-eyebrow">
            MINING ZONE
          </div>

          <h2>
            Select Mining Zone
          </h2>

          <p>
            Analyze mineral prospectivity,
            production outlook and decision intelligence.
          </p>

        </div>

        <div className="mine-selector-wrapper">

          <label htmlFor="mine-select">
            Active Mining Zone
          </label>

          <select
            id="mine-select"
            value={selectedMineId ?? ""}
            onChange={(event) =>
              setSelectedMineId(
                Number(event.target.value)
              )
            }
          >

            {data.features.map((feature) => (
              <option
                key={feature.properties.id}
                value={feature.properties.id}
              >
                {feature.properties.name}
              </option>
            ))}

          </select>

        </div>

      </section>


      {/* =================================================
          MAIN INTELLIGENCE AREA
      ================================================= */}

      <main className="intelligence-grid">

        {/* ---------------- MAP ---------------- */}

        <section className="map-card">

          <div className="card-header">

            <div>

              <span className="section-eyebrow">
                GEOSPATIAL INTELLIGENCE
              </span>

              <h2>
                Mining Zone Map
              </h2>

            </div>

            <div className="map-live">
              LIVE
            </div>

          </div>

          <div className="map-container">
            <MineMap
            data={data}
            selectedMineId={selectedMineId}
            prospectivity={prospectivity}
            onMineSelect={(mineId) => setSelectedMineId(mineId)}
             />
          </div>

        </section>


        {/* ---------------- PROSPECTIVITY ---------------- */}

        <section className="prospectivity-card">

          <ProspectivityPanel
            mineName={
              selectedMine?.properties.name ??
              "Selected Mine"
            }
            result={prospectivity}
            loading={loadingProspectivity}
            error={prospectivityError}
          />

        </section>

      </main>


      {/* =================================================
          PRODUCTION INTELLIGENCE
      ================================================= */}

      <section className="dashboard-section">

        <div className="section-heading">

          <div>

            <span className="section-eyebrow">
              PRODUCTION INTELLIGENCE
            </span>

            <h2>
              Production Outlook
            </h2>

            <p>
              Historical performance and projected
              production-demand balance.
            </p>

          </div>

          <div className="section-badge">
            2026 FORECAST
          </div>

        </div>

        <div className="production-card">

          <ProductionPanel
            data={production}
            loading={loadingProduction}
            error={productionError}
          />

        </div>

      </section>


      {/* =================================================
          DECISION SUPPORT
      ================================================= */}

      <section className="dashboard-section decision-section">

        <div className="section-heading">

          <div>

            <span className="section-eyebrow">
              AI DECISION INTELLIGENCE
            </span>

            <h2>
              Decision Support
            </h2>

            <p>
              AI-assisted recommendations for exploration
              and production planning.
            </p>

          </div>

          <div className="ai-badge">
            AI ENGINE
          </div>

        </div>

        <div className="decision-card">

          <DecisionSupportPanel
            data={decisionSupport}
            loading={loadingDecisionSupport}
            error={decisionSupportError}
          />

        </div>

      </section>


      {/* =================================================
          FOOTER
      ================================================= */}

      <footer className="mineris-footer">

        <div>
          <strong>MINERIS</strong>
          <span>
            Mineral Intelligence Platform
          </span>
        </div>

        <div>
          Decision Engine:
          <strong> AI-Assisted</strong>
        </div>

      </footer>

    </div>
  );
}