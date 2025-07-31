# constants.py

# Sti til forecast CSV
FORECAST_PATH = "data/forecast/wind.csv"

# Sti til historiske CSV'er
HISTORICAL_PATHS = {
    "wind": "data/historik/wind.csv"
}

# Antal timer vi evaluerer pr. døgn
TRADING_HOURS = list(range(24))

# Minimum spread for at tillade handel
MIN_SPREAD_THRESHOLD = 50  # i øre/MWh
