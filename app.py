# app.py
from flask import Flask, render_template, request, redirect
import pandas as pd
print("App is running")
import json
import os

app = Flask(__name__)

LOG_FILE = "latest_trade.json"
RULE_FILE = "trade_rules.json"

@app.route("/")
def index():
    trade = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            trade = json.load(f)
    return render_template("index.html", trade=trade)

@app.route("/run")
def run():
    result = run_model()
    with open(LOG_FILE, "w") as f:
        json.dump(result or {}, f)
    return redirect("/")

@app.route("/rules", methods=["GET", "POST"])
def rules():
    if request.method == "POST":
        new_rules = {
            "min_spread": float(request.form["min_spread"]),
            "allowed_buy_hours": list(map(int, request.form.getlist("allowed_buy_hours")))
        }
        with open(RULE_FILE, "w") as f:
            json.dump(new_rules, f)
        return redirect("/rules")

    rules = {"min_spread": 10.0, "allowed_buy_hours": list(range(24))}
    if os.path.exists(RULE_FILE):
        with open(RULE_FILE, "r") as f:
            rules = json.load(f)
    return render_template("rules.html", rules=rules)

if __name__ == "__main__":
    app.run(debug=True)
