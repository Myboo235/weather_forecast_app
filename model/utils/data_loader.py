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