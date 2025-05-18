import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import ARIMA
import json
from utils.data_loader import load_weather_data 
from utils.reverse_normalized import inverse_predicted_z_scores

def sarima_forecast():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")

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

    forecast = sf.forecast(df=weather_df, h=8, fitted=True)
    print("Forecast finish. Save to sarima_forecast.csv")
    forecast.to_csv("./sarima/sarima_forecast.csv")

    forecast_reverse_normalized = inverse_predicted_z_scores(forecast, "ARIMA", "../../../data/scaler.pkl")
    forecast_reverse_normalized.to_csv("./sarima/sarima_forecast_reversed.csv")

    return forecast

def sarima_forecast_next_7_days():
    weather_df = load_weather_data("../../../data/weather_normalized.csv")
    
    last_row = weather_df.tail(1)
    last_time = last_row['ds'].iloc[0].time()
    print(f"🕒 Last timestamp in data: {last_time}")
    if last_time != pd.to_datetime("21:00").time():
        print("⛔ Not last timestamp of the day. Stop predicting 7 days.")
        return

    print("✅ Last timestamp is 21:00. Proceed to predict next 7 days...")
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

    forecast = sf.forecast(df=weather_df, h=56, fitted=True)
    forecast.to_csv("./sarima/sarima_forecast_next_7d.csv", index=False)

    # Reverse normalization
    forecast_reverse_normalized = inverse_predicted_z_scores(
        forecast, 'ARIMA', "../../../data/scaler.pkl"
    )
    forecast_reverse_normalized.to_csv("./sarima/sarima_forecast_next_7d_reversed.csv", index=False)

    return forecast_reverse_normalized


sarima_forecast()
sarima_forecast_next_7_days()