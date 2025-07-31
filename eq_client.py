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
    
    print(f"▶ Fik instans: {instances[0]}")
    print(f"▶ Felter: {dir(instances[0])}")

    raise Exception("Stop her – vi tjekker felter først.")
