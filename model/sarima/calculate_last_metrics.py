import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsforecast import StatsForecast
from statsforecast.models import ARIMA
from utils.data_loader import load_weather_data 
from utils.reverse_normalized import inverse_predicted_z_scores

def calculate_last_metrics():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")

    train_df = weather_df.iloc[:-8]
    test_df = weather_df.iloc[-8:]

    with open('./sarima/sarima_parameters.json', 'r') as f:
        params = json.load(f)

    print("📦 Loaded ARIMA Parameters:")
    print(f"🔢 Order: {params['order']}")
    print(f"🌊 Seasonal Order: {params['seasonal_order']}")
    print(f"📏 Season Length: {params['season_length']}")

    sf = StatsForecast(
        models=[
            ARIMA(
                order=tuple(params['order']),
                seasonal_order=tuple(params['seasonal_order']),
                season_length=params['season_length']
            )
        ],
        freq='3h'
    )

    forecast_df = sf.forecast(df=weather_df, h=8, fitted=True)
    forecast_df.to_csv("./sarima/last_predict.csv", index=False)

    forecast_reverse_normalized = inverse_predicted_z_scores(forecast_df, "ARIMA", "../../../data/scaler.pkl")
    forecast_reverse_normalized.to_csv("./sarima/last_predict_reversed.csv", index=False)

    actual = test_df['y'].values
    predicted = forecast_df['ARIMA'].values


    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)


    metrics = {
        "rmse": rmse,
        "mse": mse,
        "mae": mae,
        "horizon": 8,
        "model": "SARIMA"
    }
    with open('./sarima/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    return metrics

calculate_last_metrics()
