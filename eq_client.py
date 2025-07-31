import os
from energyquantified import EnergyQuantified
import pandas as pd
from datetime import date, timedelta

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def get_forecast(curve_name: str):
    instances = eq.instances.list(curve=curve_name)
    if not instances:
        raise ValueError(f"No instances found for curve: {curve_name}")
    
    instance = instances[0]  # ← allerede et komplet objekt
    df = instance.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
