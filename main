# run_forecast.py
from eq_fetch import fetch_all_forecasts
from historical_loader import load_historical_data
from decision_engine import decide_trade

if __name__ == "__main__":
    live_df = fetch_all_forecasts()
    hist_df = load_historical_data()
    result = decide_trade(live_df, hist_df)

    if result:
        print(f"\n✅ Køb kl. {result['buy_hour']} → Sælg kl. {result['sell_hour']} → Forventet spread: {result['spread']} øre/MWh")
    else:
        print("\n⚠️ Ingen god handel fundet i dag.")


# eq_fetch.py
import requests
import pandas as pd
import os

API_KEY = os.getenv("EQ_API_KEY")
BASE_URL = "https://api.energyquantified.com"

curve_map = {
    "Wind": "DK1 Wind Power Production MWh/h 15min Forecast",
    "Solar": "DK1 Solar Photovoltaic Production MWh/h 15min Forecast",
    "Consumption": "DK1 Consumption MWh/h 15min Forecast",
    "ResidualLoad": "DK1 Residual Load MWh/h 15min Forecast",
    "Temperature": "DK1 Consumption Temperature °C 15min Forecast"
}

def fetch_instance_data(curve_name):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.get(f"{BASE_URL}/instances", headers=headers, params={"curve": curve_name, "limit": 1})
    r.raise_for_status()
    instances = r.json().get("items", [])
    if not instances:
        raise Exception(f"No instances found for curve: {curve_name}")

    instance_id = instances[0]["id"]
    r2 = requests.get(f"{BASE_URL}/instances/{instance_id}", headers=headers)
    r2.raise_for_status()
    data = r2.json().get("data", {})

    df = pd.DataFrame({
        "date": pd.to_datetime(data["timestamps"]),
        "value": data["values"]
    })
    df = df.resample("1H", on="date").mean().reset_index()
    df["Hour"] = df["date"].dt.hour
    return df[["Hour", "value"]]

def fetch_all_forecasts():
    dfs = []
    for label, curve in curve_map.items():
        df = fetch_instance_data(curve)
        df = df.rename(columns={"value": label})
        dfs.append(df)
    from functools import reduce
    return reduce(lambda left, right: pd.merge(left, right, on="Hour"), dfs)


# historical_loader.py
import pandas as pd
import os

def load_historical_data(folder="data/historik"):
    files = ["wind.csv", "solar.csv", "consumption.csv", "residual.csv", "temperature.csv"]
    dfs = []
    for file in files:
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        df = df.rename(columns={"value": file.replace(".csv", "").capitalize()})
        df["Hour"] = pd.to_datetime(df["date"]).dt.hour
        dfs.append(df[["Hour", df.columns[-1]]])
    from functools import reduce
    return reduce(lambda left, right: pd.merge(left, right, on="Hour"), dfs)

# decision_engine.py
import pandas as pd

def decide_trade(live_df, historical_df):
    # Sammenlign live forecast mod historisk gennemsnit pr. time
    df = pd.merge(live_df, historical_df, on="Hour", suffixes=("_live", "_hist"))
    
    df["score"] = (
        (df["ResidualLoad_live"] - df["ResidualLoad_hist"]) * 2 +
        (df["Wind_live"] - df["Wind_hist"]) * -1 +
        (df["Consumption_live"] - df["Consumption_hist"]) * 1 +
        (df["Solar_live"] - df["Solar_hist"]) * -0.5
    )
    
    # Køb = lav score (lav vind + høj residual)
    # Sælg = høj score (høj belastning, lav vind)
    buy_hour = df.loc[df["score"].idxmin(), "Hour"]
    sell_hour = df.loc[df["score"].idxmax(), "Hour"]
    spread = round(df["score"].max() - df["score"].min(), 2)

    if spread < 10:
        return None

    return {
        "buy_hour": int(buy_hour),
        "sell_hour": int(sell_hour),
        "spread": spread
    }
