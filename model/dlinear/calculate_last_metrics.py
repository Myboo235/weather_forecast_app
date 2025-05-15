import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error
from neuralforecast.models import DLinear
from neuralforecast import NeuralForecast
from utils.data_loader import load_weather_data 
from utils.reverse_normalized import inverse_predicted_z_scores

def calculate_last_metrics():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")

    train_df = weather_df.iloc[:-8]
    test_df = weather_df.iloc[-8:]

    model = DLinear(
        h=8,
        input_size=24,
        max_steps=1000,
        learning_rate=1e-3,
        val_check_steps=200,
        scaler_type='robust',
    )

    nf = NeuralForecast(models=[model], freq='3h')
    nf.fit(df=train_df)

    forecast_df = nf.predict(train_df)
    forecast_df.to_csv("./dlinear/last_predict.csv", index=False)

    forecast_reverse_normalized = inverse_predicted_z_scores(forecast_df, 'DLinear', "../../../data/scaler.pkl")
    forecast_reverse_normalized.to_csv("./dlinear/last_predict_reversed.csv", index=False)

    actual = test_df['y'].values
    predicted = forecast_df['DLinear'].values


    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)


    metrics = {
        "rmse": rmse,
        "mse": mse,
        "mae": mae,
        "horizon": 8,
        "model": "DLinear"
    }
    with open('./dlinear/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)

    return metrics

calculate_last_metrics()
