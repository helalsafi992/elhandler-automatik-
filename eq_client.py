import os
from energyquantified import EnergyQuantified
import pandas as pd
from datetime import date, timedelta

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def list_eq_curves():
    curves = eq.metadata.curves(q="dk1 forecast")
    for c in curves:
        print(c.name)

def get_forecast(curve_name: str, zone="DK1"):
    target_date = date.today() + timedelta(days=2)
    timeseries = eq.timeseries.load(
        curve = curve_name  # bruger direkte det du giver den
        begin=target_date,
        end=target_date
    )
    df = timeseries.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]].rename(columns={"value": curve_name})
