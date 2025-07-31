# strategy_engine.py
def find_best_trade(df, min_spread=50):
    best = None
    for buy_hour in range(24):
        for sell_hour in range(24):
            if sell_hour <= buy_hour:
                continue
            spread = df.loc[sell_hour, "ResidualLoad"] - df.loc[buy_hour, "ResidualLoad"]
            if spread >= min_spread:
                if not best or spread > best["spread"]:
                    best = {
                        "buy_hour": buy_hour,
                        "sell_hour": sell_hour,
                        "spread": spread
                    }
    return best
