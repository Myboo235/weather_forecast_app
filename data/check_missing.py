import pandas as pd

def load_weather_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Remove the first word (day of week) and extra year
    df['Date'] = df['Date'].str.replace(r'^[A-Za-z]+, ', '', regex=True)  # remove "Thursday, "
    df['Date'] = df['Date'].str.replace(r'(\d{4}) \1', r'\1', regex=True)  # "2009 2009" -> "2009"

    # Now safely combine and parse datetime
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d %B %Y %H:%M', errors='coerce')

    # Clean and convert temperature
    df['Temp'] = df['Temp'].str.replace('°[cC]', '', regex=True)
    df['Temp'] = df['Temp'].str.extract(r'(\d+)', expand=False).astype(float)

    # Prepare final DataFrame
    df = df[['datetime', 'Temp']].copy()
    df.columns = ['ds', 'y']

    # Set datetime index and resample
    df.set_index('ds', inplace=True)
    df = df.asfreq('3h').reset_index()

    # Add unique ID
    df['unique_id'] = 'temp_series'
    return df[['unique_id', 'ds', 'y']]


weather_df = load_weather_data("./data_batch.csv")

print(weather_df.isnull().sum())
print(weather_df[weather_df.isnull().any(axis=1)])