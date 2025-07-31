import os
from energyquantified import EnergyQuantified
import pandas as pd
from datetime import date, timedelta

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def list_eq_curves():
    curves = eq.metadata.curves(q="dk1 forecast")
    print(f"🔎 Hentede {len(curves)} kurver...\n")
    for c in curves:
        print(f"🔹 Kandidat: {c.name} – type: {getattr(c, 'curve_type', 'ukendt')}")
        if hasattr(c, "curve_type") and c.curve_type in ["TIMESERIES", "SCENARIO_TIMESERIES"]:
            print(f"✅ {c.name} [{c.curve_type}]")
            
def get_forecast(curve_name: str):
    instance = eq.instances.get_latest(curve_name)
    df = instance.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
