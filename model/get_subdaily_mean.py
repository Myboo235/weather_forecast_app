import pandas as pd

# Load data
df = pd.read_csv('data.csv', parse_dates=['datetime'])

# Create column for 'month-day hour:minute:second'
df['month_day_time'] = df['datetime'].dt.strftime('%m-%d %H:%M:%S')

# Compute mean temperature per time slot
mean_by_daytime = df.groupby('month_day_time')['temp'].mean().reset_index()
mean_by_daytime.columns = ['month_day_time', 'mean_temp']

# Merge back to original dataframe to keep both 'temp' and 'mean_temp'
df_with_mean = df.merge(mean_by_daytime, on='month_day_time')
df_with_mean.drop(columns=['month_day_time'], inplace=True)
# Save to CSV
df_with_mean.to_csv("./mean_by_subdaily.csv")
