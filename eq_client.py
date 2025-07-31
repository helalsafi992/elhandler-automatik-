import os
from energyquantified import EnergyQuantified
import pandas as pd
from datetime import date, timedelta

API_KEY = os.getenv("EQ_API_KEY")
eq = EnergyQuantified(api_key=API_KEY)

def get_forecast(curve_name: str):
    # Step 1: Find den nyeste instance for kurven
    instances = eq.instances.list(curve=curve_name)
    if not instances:
        raise ValueError(f"No instances found for curve: {curve_name}")
    
    latest_instance_id = instances[0].id  # seneste først

    # Step 2: Hent instancen
    instance = eq.instances.load_instance(instance_id=latest_instance_id)
    
    # Step 3: Konverter til dataframe
    df = instance.to_dataframe()
    df = df.resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]
