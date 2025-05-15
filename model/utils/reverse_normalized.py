import pandas as pd
import pickle
import numpy as np

normalized_data_path = "../../../data/weather_normalized.csv"
scaler_path = "../../../data/scaler.pkl"

def inverse_predicted_z_scores(df, column_name, scaler_path):
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    z_scores = df[[column_name]].values

    if hasattr(scaler, 'mean_') and len(scaler.mean_) > 1:
        dummy = np.zeros((len(z_scores), len(scaler.mean_)))
        dummy[:, 0] = z_scores.ravel()
        restored = scaler.inverse_transform(dummy)[:, 0]
    else:
        restored = scaler.inverse_transform(z_scores)

    df['temp'] = restored
    return df
