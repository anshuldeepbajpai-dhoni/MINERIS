import {
  MapContainer,
  TileLayer,
  GeoJSON,
} from "react-leaflet";

import type { Layer } from "leaflet";
import "leaflet/dist/leaflet.css";

import type { MineGeoJSON} from "../../types/mine";
import type {
  ProspectivityOverviewItem,
  ProspectivityResult,
} from "../../types/prospectivity";

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => {
    const entities: Record<string, string> = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[character];
  });
}

interface MineMapProps {
  data: MineGeoJSON;
  selectedMineId?: number | null;
  prospectivity?: ProspectivityResult | null;
  prospectivityOverview?: ProspectivityOverviewItem[];
  onMineSelect?: (mineId: number) => void;
}

export default function MineMap({
  data,
  selectedMineId,
  prospectivity,
  prospectivityOverview = [],
  onMineSelect,
}: MineMapProps) {
  const getProspectivityColor = (classification?: string) => {
    switch (classification) {
      case "HIGH":
        return "#16a34a";

      case "MEDIUM":
        return "#eab308";

      case "LOW":
        return "#dc2626";

      default:
        return "#2563eb";
    }
  };

  const getFillOpacity = (mineId: number) => {
    return mineId === selectedMineId ? 0.55 : 0.25;
  };

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
      }}
    >
      <MapContainer
        center={[21.5, 80.5]}
        zoom={6}
        style={{
          height: "600px",
          width: "100%",
          borderRadius: "12px",
        }}
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {data.features.map((feature) => {
          const mineId = feature.properties.id;
          const isSelected = mineId === selectedMineId;
          const overview = prospectivityOverview.find(
            (item) => item.mine_id === mineId
          );
          const selectedResult = isSelected ? prospectivity : null;
          const classification = selectedResult?.classification ?? overview?.classification;
          const color = getProspectivityColor(classification);
          const score = selectedResult?.prospectivity_score ?? overview?.score;
          const confidence = selectedResult?.confidence ?? overview?.confidence;

          return (
            <GeoJSON
              key={`${mineId}:${isSelected}:${classification ?? "pending"}:${score ?? "pending"}:${confidence ?? "pending"}`}
              data={feature as any}
              style={{
                color,
                weight: isSelected ? 4 : 2,
                fillColor: color,
                fillOpacity: getFillOpacity(mineId),
              }}
              onEachFeature={(_, layer: Layer) => {
                layer.on("click", () => {
                  onMineSelect?.(mineId);
                });
                const currentOverview = prospectivityOverview.find(
                  (item) => item.mine_id === mineId
                );
                const currentResult =
                  mineId === selectedMineId ? prospectivity : null;
                const prospectivityInfo = currentResult || currentOverview
                  ? `
                      <hr style="margin: 8px 0; border: 0; border-top: 1px solid #ddd;" />

                      <strong>AI Prospectivity:</strong>
                      ${currentResult?.classification ?? currentOverview?.classification}<br/>

                      <strong>Score:</strong>
                      ${currentResult?.prospectivity_score ?? currentOverview?.score}/100<br/>

                      <strong>Confidence:</strong>
                      ${currentResult?.confidence ?? currentOverview?.confidence ?? "N/A"}%
                    `
                  : `
                      <hr style="margin: 8px 0; border: 0; border-top: 1px solid #ddd;" />

                      <strong>AI Prospectivity:</strong><br/>
                      Select this mine to analyze
                    `;

                layer.bindPopup(`
                  <div style="min-width: 220px;">
                    <strong style="font-size: 16px;">
                      ${escapeHtml(feature.properties.name)}
                    </strong>

                    <br/>

                    <span style="color: #64748b;">
                      ${escapeHtml(feature.properties.location ?? "Unknown location")}
                    </span>

                    <br/><br/>

                    <strong>Area:</strong>
                    ${feature.properties.area_hectares ?? "N/A"} hectares

                    ${prospectivityInfo}
                  </div>
                `);
              }}
            />
          );
        })}
      </MapContainer>

      {/* AI Prospectivity Legend */}
      <div
        style={{
          position: "absolute",
          bottom: "24px",
          right: "16px",
          zIndex: 1000,
          background: "rgba(255, 255, 255, 0.96)",
          padding: "14px 16px",
          borderRadius: "12px",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.18)",
          minWidth: "170px",
          fontFamily:
            "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            fontWeight: 800,
            color: "#0f172a",
            letterSpacing: "0.05em",
            marginBottom: "10px",
          }}
        >
          AI PROSPECTIVITY
        </div>

        {/* HIGH */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "7px",
            fontSize: "13px",
            color: "#334155",
          }}
        >
          <span
            style={{
              width: "13px",
              height: "13px",
              borderRadius: "3px",
              background: "#16a34a",
              display: "inline-block",
            }}
          />
          <span>High</span>
        </div>

        {/* MEDIUM */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            marginBottom: "7px",
            fontSize: "13px",
            color: "#334155",
          }}
        >
          <span
            style={{
              width: "13px",
              height: "13px",
              borderRadius: "3px",
              background: "#eab308",
              display: "inline-block",
            }}
          />
          <span>Medium</span>
        </div>

        {/* LOW */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "8px",
            fontSize: "13px",
            color: "#334155",
          }}
        >
          <span
            style={{
              width: "13px",
              height: "13px",
              borderRadius: "3px",
              background: "#dc2626",
              display: "inline-block",
            }}
          />
          <span>Low</span>
        </div>

        <div
          style={{
            marginTop: "10px",
            paddingTop: "9px",
            borderTop: "1px solid #e2e8f0",
            fontSize: "11px",
            color: "#64748b",
            lineHeight: 1.4,
          }}
        >
          Mine colors show each zone's prospectivity classification. The selected mine has a thicker boundary.
        </div>
      </div>
    </div>
  );
}
