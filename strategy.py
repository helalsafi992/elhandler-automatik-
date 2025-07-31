import pandas as pd

def score_row(row):
    return (
        -0.6 * row["ResidualLoad"] +
        0.3 * row["Consumption"] +
        -0.7 * row["Wind"] +
        -0.8 * row["Solar"] +
        0.1 * row["Temperature"]
    )

def find_best_trade(df):
    df["Score"] = df.apply(score_row, axis=1)
    buy_window = df[df["Hour"].isin(range(0, 7)) | df["Hour"].isin(range(12, 15))]
    sell_window = df[df["Hour"].isin(range(17, 23))]
    best = {"spread": 0}
    for _, buy in buy_window.iterrows():
        for _, sell in sell_window.iterrows():
            spread = sell["Score"] - buy["Score"]
            if spread > 250 and spread > best["spread"]:
                best = {
                    "buy_hour": int(buy["Hour"]),
                    "sell_hour": int(sell["Hour"]),
                    "buy_score": round(buy["Score"], 2),
                    "sell_score": round(sell["Score"], 2),
                    "spread": round(spread, 2)
                }
    return best if best["spread"] > 0 else None
