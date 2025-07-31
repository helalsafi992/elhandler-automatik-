# decision_engine.py
from rules_engine import load_rules, trade_allowed

def decide_trade(live_df, historical_df):
    best_spread = -999
    best_trade = None
    rules = load_rules()

    for buy_hour in range(24):
        for sell_hour in range(buy_hour + 1, 24):
            price_buy = live_df.loc[live_df["Hour"] == buy_hour, "ResidualLoad"].values[0]
            price_sell = live_df.loc[live_df["Hour"] == sell_hour, "ResidualLoad"].values[0]
            spread = price_sell - price_buy

            if trade_allowed(buy_hour, spread, rules) and spread > best_spread:
                best_spread = spread
                best_trade = {
                    "buy_hour": buy_hour,
                    "sell_hour": sell_hour,
                    "spread": round(spread, 2)
                }

    return best_trade
