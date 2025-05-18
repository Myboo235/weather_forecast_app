import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import torch
import pandas as pd
from lstm_model import load_model
from utils.data_loader import load_normalized_data
from utils.reverse_normalized import inverse_predicted_z_scores
from utils.time_helper import get_next_hours

model_path = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
model, device = load_model(model_path)
model.eval()

def lstm_forecast():
    weather_df = load_normalized_data("../../../data/weather_normalized.csv")
    last_datetime = weather_df.index[-1]

    predictions = []
    input_seq = weather_df[-8:].values.astype('float32').copy()
    input_seq = input_seq.reshape(1, 8, -1)

    for _ in range(8):
        input_tensor = torch.from_numpy(input_seq).float().to(device)

        with torch.no_grad():
            pred = model(input_tensor)

        pred_value = pred.item()
        predictions.append(pred_value)


        input_seq = np.roll(input_seq, shift=-1, axis=1)
        input_seq[0, -1, 0] = pred_value

    # next_hours = get_next_hours()
    
    next_hours = get_next_hours(last_datetime)
    df = pd.DataFrame({
        'ds': [t.strftime("%Y-%m-%d %H:%M:%S") for t in next_hours],
        'lstm': predictions
    })
    df.to_csv("./lstm/lstm_forecast.csv", index=False)
    print("Forecast finish. Save to lstm_forecast.csv")
    forecast_reverse_normalized = inverse_predicted_z_scores(df, "lstm", "../../../data/scaler.pkl")
    forecast_reverse_normalized.to_csv("./lstm/lstm_forecast_reversed.csv", index=False)

    return df

lstm_forecast()
