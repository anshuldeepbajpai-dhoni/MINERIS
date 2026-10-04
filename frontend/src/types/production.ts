export interface ProductionHistory {
  year: number;
  planned_production: number;
  actual_production: number;
  demand: number;
}

export interface ProductionAnalysis {
  mine_id: number;
  historical_production: ProductionHistory[];

  forecast_production: number;
  forecast_demand: number;

  shortfall: number;
  shortfall_percentage: number;

  production_achievement: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
}