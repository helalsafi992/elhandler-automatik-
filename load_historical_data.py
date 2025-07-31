# load_historical_data.py
import pandas as pd
from pathlib import Path

def load_historical_data():
    path = Path("data/historical_sample.csv")
    if not path.exists():
        raise FileNotFoundError(f"Mangler datafil: {path}")

    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date")
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
