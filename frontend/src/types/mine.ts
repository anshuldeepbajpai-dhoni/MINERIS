export interface Mine {
  id: number;
  name: string;
  location: string | null;
  description: string | null;
  area_hectares: number | null;
  created_at: string;
}

export interface GeoJSONGeometry {
  type: string;
  coordinates: unknown;
}

export interface MineFeature {
  type: "Feature";
  geometry: GeoJSONGeometry | null;
  properties: {
    id: number;
    name: string;
    location: string | null;
    description: string | null;
    area_hectares: number | null;
  };
}

export interface MineGeoJSON {
  type: "FeatureCollection";
  features: MineFeature[];
}

export interface ProspectivityResult {
  id: number;
  mine_id: number;

  prospectivity_score: number;
  classification: "HIGH" | "MEDIUM" | "LOW";

  geological_score: number;
  remote_sensing_score: number;
  structural_score: number;
  historical_score: number;

  explanation: string;
  model_version: string;
  created_at: string;
}