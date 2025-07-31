from energyquantified import EnergyQuantified
from datetime import date, timedelta
import pandas as pd
import os

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def get_forecast(curve_name: str):
    instance = eq.instances.get_latest(curve_name)
    df = instance.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
