# elhandler.py
import pandas as pd
import json

def load_live_data():
    df = pd.read_csv("live_forecast.csv")  # forventet format: Hour,value
    df.columns = ["Hour", "value"]
    return df

def load_rules():
    with open("rules.json") as f:
        return json.load(f)

def find_trade(df: pd.DataFrame, rules: dict):
    min_spread = rules["min_spread"]
    allowed_buy_hours = rules["allowed_buy_hours"]

    best_trade = None
    for buy in allowed_buy_hours:
        for sell in range(buy + 1, 24):
            spread = df.loc[sell, "value"] - df.loc[buy, "value"]
            if spread >= min_spread:
                if not best_trade or spread > best_trade["spread"]:
                    best_trade = {
                        "buy_hour": buy,
                        "sell_hour": sell,
                        "spread": round(spread, 2)
                    }
    return best_trade
