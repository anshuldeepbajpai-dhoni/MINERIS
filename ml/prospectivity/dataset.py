from pathlib import Path

import numpy as np
import pandas as pd


FEATURES = [
    "geological_score",
    "remote_sensing_score",
    "structural_score",
    "historical_score",
    "elevation_score",
    "drainage_score",
]


def generate_training_dataset(
    samples: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Generate a synthetic domain-informed dataset for
    manganese prospectivity model development.

    Scores are normalized to the range 0-100.
    """

    rng = np.random.default_rng(random_state)

    geological = rng.uniform(20, 100, samples)
    remote_sensing = rng.uniform(20, 100, samples)
    structural = rng.uniform(20, 100, samples)
    historical = rng.uniform(20, 100, samples)
    elevation = rng.uniform(20, 100, samples)
    drainage = rng.uniform(20, 100, samples)

    # Domain-informed weighted signal.
    prospectivity_signal = (
        geological * 0.30
        + remote_sensing * 0.25
        + structural * 0.20
        + historical * 0.15
        + elevation * 0.05
        + drainage * 0.05
    )

    # Add small noise so the model learns a realistic boundary.
    noise = rng.normal(0, 5, samples)

    final_signal = prospectivity_signal + noise

    labels = np.where(
        final_signal >= 75,
        "HIGH",
        np.where(
            final_signal >= 50,
            "MEDIUM",
            "LOW",
        ),
    )

    df = pd.DataFrame(
        {
            "geological_score": geological,
            "remote_sensing_score": remote_sensing,
            "structural_score": structural,
            "historical_score": historical,
            "elevation_score": elevation,
            "drainage_score": drainage,
            "prospectivity_class": labels,
        }
    )

    return df.round(2)


def save_training_dataset(
    output_path: str | Path = "ml/prospectivity/data/prospectivity_training.csv",
) -> Path:

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_training_dataset()

    df.to_csv(output_path, index=False)

    return output_path


if __name__ == "__main__":
    path = save_training_dataset()

    print(f"Training dataset created: {path}")

    df = pd.read_csv(path)

    print(f"Samples: {len(df)}")
    print("\nClass distribution:")
    print(df["prospectivity_class"].value_counts())

    print("\nDataset preview:")
    print(df.head())