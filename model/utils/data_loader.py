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
