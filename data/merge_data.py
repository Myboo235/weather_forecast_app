import pandas as pd
import sys

batch_path = "./data_batch.csv"
online_path = "./data_online.csv"

try:
    # Read both files
    df_batch = pd.read_csv(batch_path)
    df_online = pd.read_csv(online_path)
except Exception as e:
    print(f"Error reading CSV files: {e}")
    sys.exit(1)

# Clean column names (remove extra whitespace)
df_batch.columns = df_batch.columns.str.strip()
df_online.columns = df_online.columns.str.strip()

# Check required columns
required_columns = {'Date', 'Time'}
if not required_columns.issubset(df_batch.columns):
    print("Error: 'Date' or 'Time' column missing in data_batch.csv")
    print("Available columns:", df_batch.columns.tolist())
    sys.exit(1)
if not required_columns.issubset(df_online.columns):
    print("Error: 'Date' or 'Time' column missing in data_online.csv")
    print("Available columns:", df_online.columns.tolist())
    sys.exit(1)

# Compare based on (Date, Time)
existing_keys = set(zip(df_batch['Date'], df_batch['Time']))
new_rows = df_online[~df_online.set_index(['Date', 'Time']).index.isin(existing_keys)]

# Append new rows if any
if not new_rows.empty:
    df_batch = pd.concat([df_batch, new_rows], ignore_index=True)
    df_batch.to_csv(batch_path, index=False)
    print(f"Appended {len(new_rows)} new rows to {batch_path}")
else:
    print("No new data to append.")
