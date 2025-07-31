from eq_client import get_forecast
from strategy import find_best_trade
import pandas as pd

def run_model(zone):
    df = pd.DataFrame({"Hour": range(24)})
    for var in ["Wind", "Solar", "ResidualLoad", "Consumption", "Temperature"]:
        fc = get_forecast(var, zone)
        df = df.merge(fc, on="Hour")
    result = find_best_trade(df)
    if result:
        print(f"{zone} → Køb kl. {result['buy_hour']}, sælg kl. {result['sell_hour']} | Spread: {result['spread']} kr/MWh")
    else:
        print(f"{zone} → Ingen god handel i dag.")

if __name__ == "__main__":
    for z in ["DK1", "DK2"]:
        run_model(z)
