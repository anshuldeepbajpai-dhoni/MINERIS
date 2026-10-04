import type { DecisionSupport } from "../../types/decisionSupport";

interface DecisionSupportPanelProps {
  data: DecisionSupport | null;
  loading: boolean;
  error: string;
}

export default function DecisionSupportPanel({
  data,
  loading,
  error,
}: DecisionSupportPanelProps) {
  if (loading) {
    return (
      <div className="decision-module">
        <div className="decision-loading">
          <div className="decision-spinner" />
          <p>Running MINERIS decision engine...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="decision-module">
        <div className="decision-error">
          <strong>Decision intelligence unavailable</strong>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="decision-module">
        <div className="decision-empty">
          No decision support data available.
        </div>
      </div>
    );
  }

  const priorityClass =
    `priority-${data.decision_priority.toLowerCase()}`;

  return (
    <div className="decision-module">

      {/* =================================================
          DECISION HEADER
      ================================================= */}

      <div className="decision-header">

        <div className="decision-title">

          <div className="ai-symbol">
            AI
          </div>

          <div>
            <span className="decision-eyebrow">
              MINERIS DECISION ENGINE
            </span>

            <h3>
              Strategic Recommendation
            </h3>

            <p>
              {data.mine_name}
            </p>
          </div>

        </div>

        <div
          className={`decision-priority ${priorityClass}`}
        >
          <span>
            DECISION PRIORITY
          </span>

          <strong>
            {data.decision_priority}
          </strong>
        </div>

      </div>


      {/* =================================================
          INTELLIGENCE SNAPSHOT
      ================================================= */}

      <div className="decision-snapshot">

        <DecisionMetric
          label="Prospectivity"
          value={`${data.prospectivity_score.toFixed(2)}/100`}
          status={data.prospectivity_classification}
          statusType="prospectivity"
        />

        <DecisionMetric
          label="Production Risk"
          value={data.production_risk}
          status={
            data.production_available
              ? "Forecast available"
              : "No production data"
          }
          statusType="risk"
        />

        <DecisionMetric
          label="Demand Gap"
          value={`${data.shortfall.toLocaleString()} t`}
          status={
            `${data.shortfall_percentage.toFixed(1)}% of demand`
          }
          statusType="gap"
        />

      </div>


      {/* =================================================
          2026 OUTLOOK
      ================================================= */}

      {data.production_available && (
        <div className="decision-outlook">

          <div className="outlook-header">

            <div>
              <span className="decision-eyebrow">
                2026 OUTLOOK
              </span>

              <h4>
                Production-Demand Balance
              </h4>
            </div>

            <span className="outlook-tag">
              FORECAST
            </span>

          </div>

          <div className="outlook-grid">

            <div className="outlook-item">
              <span>Forecast Production</span>

              <strong>
                {data.forecast_production?.toLocaleString()} t
              </strong>
            </div>

            <div className="outlook-item">
              <span>Forecast Demand</span>

              <strong>
                {data.forecast_demand?.toLocaleString()} t
              </strong>
            </div>

            <div className="outlook-item">
              <span>Projected Shortfall</span>

              <strong className="outlook-gap">
                {data.shortfall.toLocaleString()} t
              </strong>
            </div>

          </div>

          <div className="gap-progress">

            <div className="gap-progress-label">
              <span>
                Supply Coverage
              </span>

              <strong>
                {data.forecast_demand &&
                data.forecast_demand > 0
                  ? (
                      (data.forecast_production! /
                        data.forecast_demand) *
                      100
                    ).toFixed(1)
                  : "0"}
                %
              </strong>
            </div>

            <div className="gap-track">

              <div
                className="gap-fill"
                style={{
                  width: `${Math.min(
                    data.forecast_demand &&
                      data.forecast_demand > 0
                      ? (data.forecast_production! /
                          data.forecast_demand) *
                          100
                      : 0,
                    100
                  )}%`,
                }}
              />

            </div>

          </div>

        </div>
      )}


      {/* =================================================
          RECOMMENDATIONS
      ================================================= */}

      <div className="recommendation-section">

        <div className="recommendation-header">

          <div>
            <span className="decision-eyebrow">
              AI RECOMMENDATIONS
            </span>

            <h4>
              Recommended Actions
            </h4>
          </div>

          <span className="recommendation-count">
            {data.recommendations.length} ACTIONS
          </span>

        </div>


        <div className="recommendation-list">

          {data.recommendations.map(
            (recommendation, index) => (
              <div
                className="recommendation-item"
                key={index}
              >

                <div className="recommendation-number">
                  {String(index + 1).padStart(2, "0")}
                </div>

                <div className="recommendation-content">

                  <strong>
                    {getRecommendationTitle(
                      recommendation,
                      index
                    )}
                  </strong>

                  <p>
                    {recommendation}
                  </p>

                </div>

              </div>
            )
          )}

        </div>

      </div>


      {/* =================================================
          ENGINE FOOTER
      ================================================= */}

      <div className="decision-footer">

        <div>
          <span className="engine-dot" />

          Decision Engine Active
        </div>

        <span>
          Model: {data.model_version}
        </span>

      </div>

    </div>
  );
}


/* =====================================================
   DECISION METRIC
===================================================== */

function DecisionMetric({
  label,
  value,
  status,
  statusType,
}: {
  label: string;
  value: string;
  status: string;
  statusType: "prospectivity" | "risk" | "gap";
}) {
  return (
    <div className="decision-metric">

      <span className="metric-label">
        {label}
      </span>

      <strong className="metric-value">
        {value}
      </strong>

      <span
        className={`metric-status status-${statusType}`}
      >
        {status}
      </span>

    </div>
  );
}


/* =====================================================
   RECOMMENDATION TITLE
===================================================== */

function getRecommendationTitle(
  text: string,
  index: number
): string {
  const lower = text.toLowerCase();

  if (lower.includes("exploration")) {
    return "Exploration Priority";
  }

  if (
    lower.includes("production") ||
    lower.includes("capacity")
  ) {
    return "Production Intervention";
  }

  if (lower.includes("demand")) {
    return "Demand Monitoring";
  }

  if (
    lower.includes("satellite") ||
    lower.includes("geospatial") ||
    lower.includes("geological")
  ) {
    return "Intelligence Enhancement";
  }

  return `Strategic Action ${index + 1}`;
}