import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from scipy.stats import yeojohnson

# Paths
batch_path = "./data_batch.csv"
scaler_path = "./scaler.pkl"

# 1. Read data
df = pd.read_csv(batch_path)

# 2. Process Date
df["Date"] = df["Date"].fillna("").astype(str)
df["Date"] = df["Date"].str.extract(r'(\d{1,2} \w+ \d{4})')
df["Date"] = pd.to_datetime(df["Date"], format="%d %B %Y", errors="coerce")

# 3. Process Time
df["Time"] = pd.to_datetime(df["Time"], format="%H:%M", errors='coerce').dt.strftime("%H:%M")

# 4. Normalize Weather text
df["Weather"] = df["Weather"].astype(str).str.lower()

# 5. Clean numeric columns
cols_to_clean = {
    "Temp": r"[^\d.-]",
    "Rain": " mm",
    "Cloud": "%",
    "Pressure": " mb",
    "Wind": " km/h",
    "Gust": " km/h"
}

for col, pattern in cols_to_clean.items():
    df[col] = df[col].astype(str).str.replace(pattern, "", regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    if col != "Rain":
        df[col] = df[col].astype('Int64')  # Keep int type with NaNs allowed

# 6. Drop Gust column
df_cleaned = df.drop(columns=["Gust"])

# 7. Apply Yeo-Johnson transformation
df_cleaned['Wind_yeojohnson'], _ = yeojohnson(df_cleaned['Wind'].fillna(0))
df_cleaned['Rain_yeojohnson'], _ = yeojohnson(df_cleaned['Rain'].fillna(0))

# 8. Create transformed DataFrame
df_transformed = pd.DataFrame({
    'Date': df_cleaned['Date'],
    'Time': df_cleaned['Time'],
    'Weather': df_cleaned['Weather'],
    'Temp': df_cleaned['Temp'],
    'Rain': df_cleaned['Rain_yeojohnson'],
    'Cloud': df_cleaned['Cloud'],
    'Pressure': df_cleaned['Pressure'],
    'Wind': df_cleaned['Wind_yeojohnson']
})

# Save cleaned data
cleaned_data_path = "./weather_cleaned.csv"
df_transformed.to_csv(cleaned_data_path, index=False)
print(f"Saved cleaned data to {cleaned_data_path}")

# 9. Normalize selected columns
cols_to_scale = ['Temp', 'Rain', 'Cloud', 'Pressure', 'Wind']
scaler = StandardScaler()

df_scaled = df_transformed.copy()
df_scaled[cols_to_scale] = scaler.fit_transform(df_transformed[cols_to_scale])

# Save normalized data
scaled_data_path = "./weather_normalized.csv"
df_scaled.to_csv(scaled_data_path, index=False)
print(f"Saved normalized data to {scaled_data_path}")

# 10. Save the scaler
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print(f"Saved scaler to {scaler_path}")
