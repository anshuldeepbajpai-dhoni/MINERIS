import type { ProspectivityResult } from "../../types/prospectivity";

interface ProspectivityPanelProps {
  mineName: string;
  result: ProspectivityResult | null;
  loading: boolean;
  error: string;
}

export default function ProspectivityPanel({
  mineName,
  result,
  loading,
  error,
}: ProspectivityPanelProps) {
  if (loading) {
    return (
      <div className="prospectivity-panel">
        <h2>{mineName}</h2>
        <p>Running prospectivity analysis...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="prospectivity-panel">
        <h2>{mineName}</h2>
        <p style={{ color: "#dc2626" }}>{error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="prospectivity-panel">
        <h2>{mineName}</h2>
        <p>No prospectivity result available.</p>
      </div>
    );
  }

  const probabilities = result.class_probabilities
    ? Object.entries(result.class_probabilities).sort(
        ([, a], [, b]) => b - a
      )
    : [];

  const featureImportance = result.feature_importance
    ? Object.entries(result.feature_importance).sort(
        ([, a], [, b]) => b - a
      )
    : [];

  return (
    <div
      className="prospectivity-panel"
      style={{
        background: "#ffffff",
        borderRadius: "16px",
        padding: "24px",
        boxShadow: "0 10px 30px rgba(0,0,0,0.08)",
      }}
    >
      {/* Header */}
      <p
        style={{
          margin: 0,
          color: "#64748b",
          fontSize: "13px",
          fontWeight: 700,
          letterSpacing: "0.08em",
        }}
      >
        AI PROSPECTIVITY ENGINE
      </p>

      <h2 style={{ marginTop: "6px", marginBottom: "0" }}>
        {mineName}
      </h2>

      {/* Main Score */}
      <div
        style={{
          textAlign: "center",
          padding: "22px 0",
        }}
      >
        <div
          style={{
            fontSize: "52px",
            fontWeight: 800,
            lineHeight: 1,
            color: "#0f172a",
          }}
        >
          {result.prospectivity_score}
        </div>

        <div
          style={{
            color: "#64748b",
            fontSize: "13px",
            marginTop: "6px",
          }}
        >
          ML Prospectivity Score / 100
        </div>

        <div
          style={{
            display: "inline-block",
            marginTop: "14px",
            padding: "7px 20px",
            borderRadius: "20px",
            fontWeight: 800,
            fontSize: "13px",
            letterSpacing: "0.04em",
            background:
              result.classification === "HIGH"
                ? "#dcfce7"
                : result.classification === "MEDIUM"
                  ? "#fef3c7"
                  : "#fee2e2",
            color:
              result.classification === "HIGH"
                ? "#166534"
                : result.classification === "MEDIUM"
                  ? "#92400e"
                  : "#991b1b",
          }}
        >
          {result.classification} PROSPECTIVITY
        </div>
      </div>

      {/* Confidence */}
      {result.confidence !== null && (
        <div
          style={{
            padding: "16px",
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            borderRadius: "12px",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "8px",
            }}
          >
            <span
              style={{
                fontWeight: 700,
                color: "#334155",
              }}
            >
              ML Confidence
            </span>

            <strong>{result.confidence.toFixed(1)}%</strong>
          </div>

          <div
            style={{
              height: "9px",
              background: "#e2e8f0",
              borderRadius: "10px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${Math.min(result.confidence, 100)}%`,
                height: "100%",
                background: "#16a34a",
                borderRadius: "10px",
              }}
            />
          </div>
        </div>
      )}

      {/* Class Probabilities */}
      {probabilities.length > 0 && (
        <>
          <SectionTitle title="Class Probability" />

          <div style={{ marginBottom: "24px" }}>
            {probabilities.map(([label, value]) => (
              <ProbabilityBar
                key={label}
                label={label}
                value={value}
              />
            ))}
          </div>
        </>
      )}

      {/* Analysis Factors */}
      <SectionTitle title="Analysis Factors" />

      <ScoreBar
        label="Geological"
        value={result.geological_score}
      />

      <ScoreBar
        label="Remote Sensing"
        value={result.remote_sensing_score}
      />

      <ScoreBar
        label="Structural"
        value={result.structural_score}
      />

      <ScoreBar
        label="Historical"
        value={result.historical_score}
      />

      {/* Feature Importance */}
      {featureImportance.length > 0 && (
        <>
          <SectionTitle title="Top Contributing Features" />

          <div style={{ marginBottom: "24px" }}>
            {featureImportance.slice(0, 6).map(
              ([feature, value]) => (
                <ImportanceBar
                  key={feature}
                  label={formatFeatureName(feature)}
                  value={value}
                />
              )
            )}
          </div>
        </>
      )}

      {/* AI Explanation */}
      <SectionTitle title="AI Explanation" />

      <div
        style={{
          background: "#f8fafc",
          borderLeft: "4px solid #2563eb",
          borderRadius: "8px",
          padding: "14px 16px",
          marginTop: "10px",
        }}
      >
        <p
          style={{
            margin: 0,
            color: "#475569",
            lineHeight: 1.65,
            fontSize: "14px",
          }}
        >
          {result.explanation}
        </p>
      </div>

      {/* Model Footer */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "12px",
          marginTop: "22px",
          paddingTop: "14px",
          borderTop: "1px solid #e2e8f0",
          fontSize: "11px",
          color: "#94a3b8",
        }}
      >
        <span>MODEL</span>

        <strong
          style={{
            color: "#64748b",
          }}
        >
          {result.model_version}
        </strong>
      </div>
    </div>
  );
}

/* ----------------------------- */
/* Section Title                 */
/* ----------------------------- */

function SectionTitle({ title }: { title: string }) {
  return (
    <h3
      style={{
        marginTop: "22px",
        marginBottom: "14px",
        fontSize: "15px",
        color: "#0f172a",
      }}
    >
      {title}
    </h3>
  );
}

/* ----------------------------- */
/* Score Bar                     */
/* ----------------------------- */

interface ScoreBarProps {
  label: string;
  value: number;
}

function ScoreBar({ label, value }: ScoreBarProps) {
  return (
    <div style={{ marginBottom: "15px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "5px",
          fontSize: "13px",
        }}
      >
        <span>{label}</span>

        <strong>{value.toFixed(1)}</strong>
      </div>

      <div
        style={{
          height: "8px",
          background: "#e2e8f0",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${Math.min(value, 100)}%`,
            height: "100%",
            background: "#2563eb",
            borderRadius: "10px",
          }}
        />
      </div>
    </div>
  );
}

/* ----------------------------- */
/* Probability Bar               */
/* ----------------------------- */

function ProbabilityBar({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  const normalizedLabel = label.toUpperCase();

  const background =
    normalizedLabel === "HIGH"
      ? "#16a34a"
      : normalizedLabel === "MEDIUM"
        ? "#d97706"
        : "#dc2626";

  return (
    <div style={{ marginBottom: "13px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "5px",
          fontSize: "13px",
        }}
      >
        <span
          style={{
            fontWeight: 600,
            color: "#334155",
          }}
        >
          {normalizedLabel}
        </span>

        <strong>{value.toFixed(1)}%</strong>
      </div>

      <div
        style={{
          height: "8px",
          background: "#e2e8f0",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${Math.min(value, 100)}%`,
            height: "100%",
            background,
            borderRadius: "10px",
            transition: "width 0.4s ease",
          }}
        />
      </div>
    </div>
  );
}

/* ----------------------------- */
/* Feature Importance             */
/* ----------------------------- */

function ImportanceBar({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div style={{ marginBottom: "13px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "5px",
          fontSize: "13px",
        }}
      >
        <span>{label}</span>

        <strong>{value.toFixed(1)}%</strong>
      </div>

      <div
        style={{
          height: "7px",
          background: "#e2e8f0",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${Math.min(value, 100)}%`,
            height: "100%",
            background: "#7c3aed",
            borderRadius: "10px",
          }}
        />
      </div>
    </div>
  );
}

/* ----------------------------- */
/* Feature Name Formatter         */
/* ----------------------------- */

function formatFeatureName(feature: string) {
  return feature
    .replace(/_score$/, "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}