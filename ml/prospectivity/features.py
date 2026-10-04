from dataclasses import dataclass


@dataclass
class ProspectivityFeatures:
    geological_score: float
    remote_sensing_score: float
    structural_score: float
    historical_score: float
    elevation_score: float
    drainage_score: float

    def as_dict(self) -> dict[str, float]:
        return {
            "geological_score": self.geological_score,
            "remote_sensing_score": self.remote_sensing_score,
            "structural_score": self.structural_score,
            "historical_score": self.historical_score,
            "elevation_score": self.elevation_score,
            "drainage_score": self.drainage_score,
        }