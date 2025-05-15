import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# # Test run
sarima_forecast()