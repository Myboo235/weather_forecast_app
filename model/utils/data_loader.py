import os
import pandas as pd
import pickle

def process_data(df):
    df = df.copy()

    if "Date" in df.columns and "Time" in df.columns:
        df["Formatted Date"] = df["Date"].astype(str) + " " + df["Time"].astype(str)
        df = df.drop(columns=["Date", "Time"])
        df = df.set_index(pd.DatetimeIndex(df["Formatted Date"]))
        df = df.drop(["Formatted Date", "Weather"], axis=1, errors="ignore")
        df.index.name = "date"
        return df
    else:
        print("DataFrame dont have 'Date' or 'Time'.")
        return df


def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), "..", "data", filename)


def load_normalized_data(path):
    # path = ("/data/weather_normalized.csv")
    df_normalized = pd.read_csv(path)
    df_normalized = process_data(df_normalized)
    return df_normalized


def load_historical_data():
    path = get_data_path("/data/weather_cleaned.csv")
    df_online = pd.read_csv(path)
    df_online = process_data(df_online)
    return df_online


def load_scaler():
    path = get_data_path("/data/scaler.pkl")
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Scaler file not exist: {path}")
        return None


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [("var%d(t-%d)" % (j + 1, i)) for j in range(n_vars)]
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [("var%d(t)" % (j + 1)) for j in range(n_vars)]
        else:
            names += [("var%d(t+%d)" % (j + 1, i)) for j in range(n_vars)]

    agg = pd.concat(cols, axis=1)
    agg.columns = names

    if dropnan:
        agg.dropna(inplace=True)
    return agg


def create_dataset(dataset, n_hours, n_features, n_predict):
    data = dataset.values
    data = data.astype("float32")

    reframed = series_to_supervised(data, n_hours, n_predict)
    reframed = reframed.values

    dataX = reframed[:, : n_hours * n_features]
    dataY = reframed[:, -n_features]

    dataX = dataX.reshape(dataX.shape[0], n_hours, n_features)

    return dataX, dataY


def load_retrain_data():
    path = get_data_path("/data/weather_normalized.csv")
    df = pd.read_csv(path)
    df = process_data(df)
    end_date = pd.Timestamp.now().normalize()
    start_date = end_date - pd.Timedelta(days=7)

    mask = (df.index >= start_date) & (df.index < end_date)
    df_new = df.loc[mask]
    return df_new