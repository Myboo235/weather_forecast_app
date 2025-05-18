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
        input_size=24,
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


    # Filter to the last row with time 21:00
    last_21 = weather_df[weather_df['ds'].dt.time == pd.to_datetime("21:00").time()].iloc[-1]

    print(last_21)
    # Extract the unique_id and timestamp of that last 21:00
    # last_uid = last_21['unique_id']
    # last_time = last_21['ds']

    # # Get the 24 input steps ending at that time
    # # cutoff_time = last_time
    # # input_df = weather_df[
    # #     (weather_df['unique_id'] == last_uid) &
    # #     (weather_df['ds'] <= cutoff_time)
    # # ].tail(24)  # last 24 steps for input

    # # Initialize model
    # model = DLinear(
    #     h=56,  # 7 days * 8 steps/day
    #     input_size=24,
    #     max_steps=1000,
    #     learning_rate=1e-3,
    #     val_check_steps=200,
    #     scaler_type='robust',
    # )

    # nf = NeuralForecast(models=[model], freq='3h')
    # nf.fit(df=weather_df)  # Train on all available data

    # # Forecast starting from the last 24 steps
    # forecast_df = nf.predict(future_df=input_df)
    # forecast_df.to_csv("./dlinear/dlinear_forecast_next_7d.csv", index=False)

    # # Reverse normalization
    # forecast_reverse_normalized = inverse_predicted_z_scores(
    #     forecast_df, 'DLinear', "../../../data/scaler.pkl"
    # )
    # forecast_reverse_normalized.to_csv("./dlinear/dlinear_forecast_next_7d_reversed.csv", index=False)

    # return forecast_reverse_normalized

dlinear_forecast()
# dlinear_forecast_next_7_days()
