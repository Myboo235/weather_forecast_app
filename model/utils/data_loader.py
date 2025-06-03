import pandas as pd

def load_weather_data(path: str) -> pd.DataFrame:
    """Load and process weather CSV data for StatsForecast."""
    df = pd.read_csv(path)

    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df = df[['datetime', 'Temp']].copy()
    df.columns = ['ds', 'y']

    df.set_index('ds', inplace=True)
    df = df.asfreq('3h').reset_index()

    df['unique_id'] = 'temp_series'
    return df[['unique_id', 'ds', 'y']]

def process_data(df):
    df = df.copy()
    
    if 'Date' in df.columns and 'Time' in df.columns:
        df["Formatted Date"] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)
        df = df.drop(columns=["Date", "Time"])
        df = df.set_index(pd.DatetimeIndex(df['Formatted Date']))
        df = df.drop(['Formatted Date', 'Weather'], axis=1, errors='ignore')
        df.index.name = 'date'
        return df
    else:
        print("DataFrame dont have 'Date' or 'Time'.")
        return df

def load_normalized_data(path):
    df_normalized = pd.read_csv(path)
    df_normalized = process_data(df_normalized)
    # df_normalized.values.astype('float32')

    return df_normalized

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
    df = pd.read_csv("/data/weather_normalized.csv")
    df = process_data(df)
    end_date = pd.Timestamp.now().normalize()
    start_date = end_date - pd.Timedelta(days=7)

    mask = (df.index >= start_date) & (df.index < end_date)
    df_new = df.loc[mask]
    return df_new

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
