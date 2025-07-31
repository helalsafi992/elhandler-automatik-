from eq_client import get_forecast
from strategy import find_best_trade
import pandas as pd

def run_model(zone):
    print(f"\n⚡ Kører elhandelsmodel for {zone}...\n")

    df = pd.DataFrame({"Hour": range(24)})

    # Gyldige kurver til EQ v0.14.6 og timeseries.load()
    curve_map = {
        "Wind": "Forecasts DK1 Wind Power MWh/h",
        "Solar": "Forecasts DK1 Solar Power MWh/h",
        "Consumption": "Forecasts DK1 Consumption MWh/h",
        "ResidualLoad": "Forecasts DK1 Residual Load MWh/h",
        "Temperature": "Forecasts DK1 Temperature °C"
    }

    for var, curve in curve_map.items():
        fc = get_forecast(curve)
        df = df.merge(fc.rename(columns={"value": var}), on="Hour")

    result = find_best_trade(df)
    if result:
        print(f"✅ {zone} → Køb kl. {result['buy_hour']}, sælg kl. {result['sell_hour']} | Spread: {result['spread']} kr/MWh\n")
    else:
        print(f"⚠️ {zone} → Ingen god handel fundet i dag.\n")

if __name__ == "__main__":
    run_model("DK1")
