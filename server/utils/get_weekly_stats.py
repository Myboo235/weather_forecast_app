import pandas as pd

def get_daily_min_max(origin_df):
    df = origin_df.copy()

    df["date"] = pd.to_datetime(df["ds"]).dt.date
    return df.groupby("date")["temp"].agg(["min", "max"]).reset_index()
