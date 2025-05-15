import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

dlinear_forecast()
