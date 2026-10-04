import type { ProductionAnalysis } from "../../types/production";

interface ProductionPanelProps {
  data: ProductionAnalysis | null;
  loading: boolean;
  error: string;
}

export default function ProductionPanel({
  data,
  loading,
  error,
}: ProductionPanelProps) {
  if (loading) {
    return (
      <div className="production-module">
        <div className="production-loading">
          <div className="production-spinner" />
          <p>Analyzing production data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="production-module">
        <div className="production-error">
          <strong>Production analysis unavailable</strong>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="production-module">
        <div className="production-empty">
          No production data available.
        </div>
      </div>
    );
  }

  const latestYear =
    data.historical_production[
      data.historical_production.length - 1
    ]?.year;

  return (
    <div className="production-module">

      {/* ============================================
          KPI ROW
      ============================================ */}

      <div className="production-kpis">

        <KpiCard
          label="2026 Forecast"
          value={`${data.forecast_production.toLocaleString()} t`}
          description="Projected production"
          type="primary"
        />

        <KpiCard
          label="Projected Demand"
          value={`${data.forecast_demand.toLocaleString()} t`}
          description="Expected requirement"
        />

        <KpiCard
          label="Demand Gap"
          value={`${data.shortfall.toLocaleString()} t`}
          description={`${data.shortfall_percentage.toFixed(1)}% of demand`}
          type={
            data.shortfall_percentage > 10
              ? "danger"
              : data.shortfall_percentage > 5
                ? "warning"
                : "success"
          }
        />

        <KpiCard
          label="Achievement"
          value={`${data.production_achievement.toFixed(2)}%`}
          description="Historical plan achievement"
          type={
            data.production_achievement >= 90
              ? "success"
              : data.production_achievement >= 75
                ? "warning"
                : "danger"
          }
        />

      </div>


      {/* ============================================
          FORECAST SUMMARY
      ============================================ */}

      <div className="production-summary">

        <div className="production-summary-main">

          <div className="production-summary-label">
            PRODUCTION VS DEMAND
          </div>

          <h3>
            {latestYear
              ? `${latestYear} Historical Performance`
              : "Historical Performance"}
          </h3>

          <p>
            Production trajectory compared with projected
            mineral demand.
          </p>

        </div>

        <div className="production-risk">

          <span className="risk-label">
            PRODUCTION RISK
          </span>

          <span
            className={`risk-badge risk-${data.risk_level.toLowerCase()}`}
          >
            {data.risk_level}
          </span>

        </div>

      </div>


      {/* ============================================
          TREND VISUALIZATION
      ============================================ */}

      <ProductionTrend data={data} />


      {/* ============================================
          HISTORICAL TABLE
      ============================================ */}

      <div className="production-history">

        <div className="history-header">

          <div>
            <span className="history-eyebrow">
              HISTORICAL DATA
            </span>

            <h3>
              Production Performance
            </h3>
          </div>

          <span className="history-unit">
            Unit: tonnes
          </span>

        </div>

        <div className="production-table-wrapper">

          <table className="production-table">

            <thead>
              <tr>
                <th>Year</th>
                <th>Planned</th>
                <th>Actual</th>
                <th>Demand</th>
                <th>Achievement</th>
                <th>Gap</th>
              </tr>
            </thead>

            <tbody>

              {data.historical_production.map(
                (record) => {

                  const achievement =
                    record.planned_production > 0
                      ? (record.actual_production /
                          record.planned_production) *
                        100
                      : 0;

                  const gap = Math.max(
                    record.demand -
                      record.actual_production,
                    0
                  );

                  return (
                    <tr key={record.year}>

                      <td>
                        <strong>
                          {record.year}
                        </strong>
                      </td>

                      <td>
                        {record.planned_production.toLocaleString()}
                      </td>

                      <td>
                        <strong>
                          {record.actual_production.toLocaleString()}
                        </strong>
                      </td>

                      <td>
                        {record.demand.toLocaleString()}
                      </td>

                      <td>
                        <span
                          className={
                            achievement >= 90
                              ? "achievement-good"
                              : achievement >= 75
                                ? "achievement-medium"
                                : "achievement-low"
                          }
                        >
                          {achievement.toFixed(1)}%
                        </span>
                      </td>

                      <td>
                        <span
                          className={
                            gap > 0
                              ? "gap-value"
                              : "gap-zero"
                          }
                        >
                          {gap.toLocaleString()}
                        </span>
                      </td>

                    </tr>
                  );
                }
              )}

            </tbody>

          </table>

        </div>

      </div>


      {/* ============================================
          FORECAST NOTE
      ============================================ */}

      <div className="production-note">

        <div className="note-icon">
          i
        </div>

        <div>

          <strong>
            Forecast methodology
          </strong>

          <p>
            The current baseline forecast extrapolates
            the average year-over-year change from available
            historical production and demand records.
            This will be replaced by the trained forecasting
            model in the ML layer.
          </p>

        </div>

      </div>

    </div>
  );
}


/* =====================================================
   KPI CARD
===================================================== */

function KpiCard({
  label,
  value,
  description,
  type = "default",
}: {
  label: string;
  value: string;
  description: string;
  type?: "default" | "primary" | "success" | "warning" | "danger";
}) {
  return (
    <div className={`production-kpi kpi-${type}`}>

      <div className="kpi-label">
        {label}
      </div>

      <div className="kpi-value">
        {value}
      </div>

      <div className="kpi-description">
        {description}
      </div>

    </div>
  );
}


/* =====================================================
   TREND VISUALIZATION
===================================================== */

function ProductionTrend({
  data,
}: {
  data: ProductionAnalysis;
}) {
  const records = data.historical_production;

  const allValues = records.flatMap((record) => [
    record.actual_production,
    record.demand,
  ]);

  const maxValue =
    Math.max(...allValues, data.forecast_demand);

  const minValue =
    Math.min(...allValues, data.forecast_production);

  const range =
    Math.max(maxValue - minValue, 1);

  const chartWidth = 800;
  const chartHeight = 260;

  const paddingLeft = 55;
  const paddingRight = 25;
  const paddingTop = 25;
  const paddingBottom = 45;

  const plotWidth =
    chartWidth -
    paddingLeft -
    paddingRight;

  const plotHeight =
    chartHeight -
    paddingTop -
    paddingBottom;

  const getX = (index: number) => {
    if (records.length <= 1) {
      return paddingLeft;
    }

    return (
      paddingLeft +
      (index /
        (records.length - 1)) *
        plotWidth
    );
  };

  const getY = (value: number) => {
    return (
      paddingTop +
      ((maxValue - value) / range) *
        plotHeight
    );
  };

  const actualPoints = records
    .map(
      (record, index) =>
        `${getX(index)},${getY(
          record.actual_production
        )}`
    )
    .join(" ");

  const demandPoints = records
    .map(
      (record, index) =>
        `${getX(index)},${getY(
          record.demand
        )}`
    )
    .join(" ");

  return (
    <div className="production-chart">

      <div className="chart-legend">

        <span>
          <i className="legend-dot actual" />
          Actual Production
        </span>

        <span>
          <i className="legend-dot demand" />
          Demand
        </span>

      </div>

      <div className="chart-wrapper">

        <svg
          viewBox={`0 0 ${chartWidth} ${chartHeight}`}
          preserveAspectRatio="none"
          className="production-svg"
        >

          {/* Grid */}

          {[0, 1, 2, 3, 4].map(
            (line) => {

              const y =
                paddingTop +
                (line / 4) *
                  plotHeight;

              return (
                <line
                  key={line}
                  x1={paddingLeft}
                  y1={y}
                  x2={
                    chartWidth -
                    paddingRight
                  }
                  y2={y}
                  className="chart-grid"
                />
              );
            }
          )}


          {/* Actual line */}

          <polyline
            points={actualPoints}
            className="actual-line"
            fill="none"
          />


          {/* Demand line */}

          <polyline
            points={demandPoints}
            className="demand-line"
            fill="none"
          />


          {/* Actual points */}

          {records.map(
            (record, index) => (
              <circle
                key={`actual-${record.year}`}
                cx={getX(index)}
                cy={getY(
                  record.actual_production
                )}
                r="5"
                className="actual-point"
              />
            )
          )}


          {/* Demand points */}

          {records.map(
            (record, index) => (
              <circle
                key={`demand-${record.year}`}
                cx={getX(index)}
                cy={getY(
                  record.demand
                )}
                r="4"
                className="demand-point"
              />
            )
          )}


          {/* Year labels */}

          {records.map(
            (record, index) => (
              <text
                key={record.year}
                x={getX(index)}
                y={
                  chartHeight -
                  16
                }
                textAnchor="middle"
                className="chart-label"
              >
                {record.year}
              </text>
            )
          )}

        </svg>

      </div>

      {/* Forecast */}

      <div className="forecast-strip">

        <span>
          <strong>2026 Forecast</strong>
        </span>

        <span>
          Production:
          <strong>
            {data.forecast_production.toLocaleString()} t
          </strong>
        </span>

        <span>
          Demand:
          <strong>
            {data.forecast_demand.toLocaleString()} t
          </strong>
        </span>

        <span
          className={
            data.shortfall > 0
              ? "forecast-gap"
              : "forecast-balanced"
          }
        >
          Gap:
          <strong>
            {data.shortfall.toLocaleString()} t
          </strong>
        </span>

      </div>

    </div>
  );
}