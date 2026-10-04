export interface DecisionSupport {
  mine_id: number;
  mine_name: string;

  prospectivity_score: number;
  prospectivity_classification: "LOW" | "MEDIUM" | "HIGH";

  production_available: boolean;

  forecast_production: number | null;
  forecast_demand: number | null;

  shortfall: number;
  shortfall_percentage: number;

  production_risk: "LOW" | "MEDIUM" | "HIGH" | "UNKNOWN";

  decision_priority:
    | "LOW"
    | "MEDIUM"
    | "HIGH"
    | "CRITICAL";

  recommendations: string[];

  model_version: string;
}