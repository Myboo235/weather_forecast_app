import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from neuralforecast.models import DLinear
from neuralforecast import NeuralForecast
from utils.data_loader import load_weather_data 
from utils.reverse_normalized import inverse_predicted_z_scores

def dlinear_forecast():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")
    model = DLinear(
        h=8,
        input_size=8,
        max_steps=1000,
        learning_rate=1e-3,
        val_check_steps=200,
        scaler_type='robust',
    )

    nf = NeuralForecast(models=[model], freq='3h')
    nf.fit(df=weather_df)

    forecast_df = nf.predict(weather_df)
    forecast_df.to_csv("./dlinear/dlinear_forecast.csv")

    forecast_reverse_normalized = inverse_predicted_z_scores(forecast_df, 'DLinear', "../../../data/scaler.pkl")
    forecast_reverse_normalized.to_csv("./dlinear/dlinear_forecast_reversed.csv", index=False)

    return forecast_df

def dlinear_forecast_next_7_days():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")
    
    last_row = weather_df.tail(1)
    last_time = last_row['ds'].iloc[0].time()
    print(f"🕒 Last timestamp in data: {last_time}")
    if last_time != pd.to_datetime("21:00").time():
        print("⛔ Not last timestamp of the day. Stop predicting 7 days.")
        return

    print("✅ Last timestamp is 21:00. Proceed to predict next 7 days...")
    model = DLinear(
        h=56,  # 7 days * 8 steps/day
        input_size=8,
        max_steps=1000,
        learning_rate=1e-3,
        val_check_steps=200,
        scaler_type='robust',
    )

    nf = NeuralForecast(models=[model], freq='3h')
    nf.fit(df=weather_df)

    forecast_df = nf.predict()
    forecast_df.to_csv("./dlinear/dlinear_forecast_next_7d.csv", index=False)

    # Reverse normalization
    forecast_reverse_normalized = inverse_predicted_z_scores(
        forecast_df, 'DLinear', "../../../data/scaler.pkl"
    )
    forecast_reverse_normalized.to_csv("./dlinear/dlinear_forecast_next_7d_reversed.csv", index=False)

    return forecast_reverse_normalized

dlinear_forecast()
dlinear_forecast_next_7_days()
