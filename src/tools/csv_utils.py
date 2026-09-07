from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "seed"


def read_csv(filename: str) -> pd.DataFrame:
    """Read a CSV file from the seed data directory."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    return pd.read_csv(file_path)


def append_csv(filename: str, row: dict) -> None:
    """Append one record to a CSV file."""
    file_path = DATA_DIR / filename

    df = pd.DataFrame([row])
    df.to_csv(
        file_path,
        mode="a",
        header=not file_path.exists(),
        index=False,
    )