# strategy_engine.py
def find_best_trade(df):
    best = {"spread": 0, "buy_hour": None, "sell_hour": None}

    for buy_hour in range(24):
        for sell_hour in range(buy_hour + 1, 24):
            spread = df.loc[sell_hour, "ResidualLoad"] - df.loc[buy_hour, "ResidualLoad"]

            if spread > best["spread"]:
                best["spread"] = round(spread, 2)
                best["buy_hour"] = int(buy_hour)
                best["sell_hour"] = int(sell_hour)

    if best["spread"] >= 50:  # eksempelregel – kan flyttes til rules.json
        return best
    return None
import pandas as pd
from forecast_engine import get_forecast  # eller tilpas til hvor forecast kommer fra

def run_model():
    df = get_forecast()  # hent dataframe med ResidualLoad pr. time
    result = find_best_trade(df)
    return result
