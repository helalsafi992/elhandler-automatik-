# app.py (hovedfil til Render)
from flask import Flask, render_template, request, redirect
import os
import json
from datetime import datetime
from run_forecast import run_strategy

app = Flask(__name__)

MEMORY_FILE = "memory.json"

# Sørg for at fil findes
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

@app.route("/")
def index():
    with open(MEMORY_FILE) as f:
        memory = json.load(f)
    latest = memory[-1] if memory else None
    return render_template("index.html", latest=latest)

@app.route("/run")
def run():
    result = run_strategy()
    with open(MEMORY_FILE) as f:
        memory = json.load(f)
    memory.append({"timestamp": datetime.now().isoformat(), **result})
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    return redirect("/")

@app.route("/rules", methods=["GET", "POST"])
def rules():
    if request.method == "POST":
        rules = {
            "min_spread": float(request.form["min_spread"]),
            "allowed_buy_hours": request.form["allowed_buy_hours"].split(",")
        }
        with open("rules.json", "w") as f:
            json.dump(rules, f, indent=2)
        return redirect("/")
    else:
        if os.path.exists("rules.json"):
            with open("rules.json") as f:
                rules = json.load(f)
        else:
            rules = {"min_spread": 8.0, "allowed_buy_hours": ["0", "1", "2", "3", "4", "12", "13", "14"]}
        return render_template("rules.html", rules=rules)

if __name__ == "__main__":
    app.run(debug=True)
