# forecast_engine.py
import pandas as pd
from datetime import datetime, timedelta

def fetch_latest_forecast(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] >= datetime.now().replace(minute=0, second=0, microsecond=0)]
    df = df.set_index("date").resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
import pandas as pd
import numpy as np

def get_forecast():
    # Dummy-data: ResidualLoad for 24 timer
    df = pd.DataFrame({
        "ResidualLoad": np.random.randint(1000, 2000, size=24)
    })
    return df
