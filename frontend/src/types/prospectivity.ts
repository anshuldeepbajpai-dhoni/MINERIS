export interface ProspectivityResult {
  id: number;
  mine_id: number;

  prospectivity_score: number;
  classification: "LOW" | "MEDIUM" | "HIGH";

  geological_score: number;
  remote_sensing_score: number;
  structural_score: number;
  historical_score: number;

  confidence: number | null;

  class_probabilities: Record<string, number> | null;

  feature_importance: Record<string, number> | null;

  explanation: string;

  model_version: string;
  created_at: string;
}

export interface ProspectivityOverviewItem {
  mine_id: number;
  mine_name: string;
  score: number;
  classification: "LOW" | "MEDIUM" | "HIGH";
  confidence: number | null;
  model_version: string;
}