import os
from energyquantified import EnergyQuantified
import pandas as pd
from datetime import date, timedelta

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def get_forecast(curve_name: str):
    # Step 1: Find instansliste (metadata)
    instance_meta_list = eq.instances.list(curve=curve_name)
    if not instance_meta_list:
        raise ValueError(f"No instances found for curve: {curve_name}")
    
    # Step 2: Brug metadata til at finde ID
    instance_meta = instance_meta_list[0]
    instance = eq.instances.load_instance(instance_meta)

    # Step 3: Konverter til DataFrame
    df = instance.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
