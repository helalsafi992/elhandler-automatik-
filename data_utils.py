# data_utils.py
import pandas as pd

def load_csv(path):
    df = pd.read_csv(path, parse_dates=["date"])
    df["Hour"] = df["date"].dt.hour
    return df

def average_per_hour(df):
    return df.groupby("Hour")["value"].mean().reset_index()
