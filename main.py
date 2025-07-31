from eq_client import get_forecast
from strategy import find_best_trade
import pandas as pd

def run_model(zone):
    print(f"\n⚡ Kører elhandelsmodel for {zone}...\n")

    df = pd.DataFrame({"Hour": range(24)})

    # Rigtige EQ-kurver (bekræftet i logs)
    curve_map = {
        "Wind": "DK1 Wind Power Production MWh/h 15min Forecast",
        "Solar": "DK1 Solar Photovoltaic Production MWh/h 15min Forecast",
        "Consumption": "DK1 Consumption MWh/h 15min Forecast",
        "ResidualLoad": "DK1 Residual Load MWh/h 15min Forecast",
        "Temperature": "DK1 Consumption Temperature °C 15min Forecast"
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
