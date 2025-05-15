import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
from statsforecast.arima import arima_string
import json
import datetime
from utils.data_loader import load_weather_data 

weather_df = load_weather_data("../../../data/weather_normalized.csv")

season_length = 8
sf = StatsForecast(
    models=[AutoARIMA(
        seasonal=True,
        season_length=season_length,
        start_p=1, start_q=1,
        max_p=3, max_q=3,
        start_P=1, start_Q=1,
        max_P=2, max_Q=2,
        d=None, D=None,
        trace=True,
        stepwise=True,
    )],
    freq='3h',
)
sf.fit(df=weather_df)

best_model = sf.fitted_[0, 0].model_
print("✅ Best model:", arima_string(best_model))

def extract_parameters(model):
    order = tuple(model["arma"][i] for i in [0, 5, 1, 2, 6, 3, 4])
    p, d, q, P, D, Q, m = order
    return {
        "order": (p, d, q),
        "seasonal_order": (P, D, Q),
        "season_length": m,
        "aic": model["aic"],
        "model_string": arima_string(model),
        "timestamp": datetime.datetime.now().isoformat()
    }


params = extract_parameters(best_model)

# This script is intended to be run from the project root directory
# (e.g., when used in GitHub Actions), so relative paths like ./sarima/... are correct
# Save as current version
with open("./sarima/sarima_parameters.json", "w") as f:
    json.dump(params, f, indent=2)

# Append to history file (JSON Lines format)
with open("./sarima/sarima_parameters_history.jsonl", "a") as f:
    f.write(json.dumps(params) + "\n")

print("💾 Saved best ARIMA parameters to sarima_parameters.json")