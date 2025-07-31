# utils.py
import pandas as pd

def clean_and_resample(df):
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").resample("1H").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df
