from energyquantified import EnergyQuantified
from datetime import date, timedelta
import pandas as pd
import os

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def get_forecast(curve_name: str):
    target_date = date.today() + timedelta(days=2)
    timeseries = eq.timeseries.load(
        curve=curve_name,
        begin=target_date,
        end=target_date
    )
    df = timeseries.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
