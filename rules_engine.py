# rules_engine.py
import json

def load_rules(path="rules.json"):
    with open(path, "r") as f:
        return json.load(f)

def trade_allowed(buy_hour, spread, rules):
    if spread < rules["min_spread"]:
        return False
    if buy_hour not in rules["allowed_buy_hours"]:
        return False
    return True
