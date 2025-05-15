import sys
import os

sys.path.append(os.path.abspath("/"))
# from model.lstm.predictor import recursive_forecast
# from model.sarima.sarima_forecast import sarima_forecast

import numpy as np
from flask import request
from flask_restx import Namespace, Resource

from utils.time_helper import get_next_hours
from utils.data_loader import load_normalized_data, load_historical_data, load_scaler
from .schemas import register_models
import config as cfg
import pandas as pd

ns = Namespace("api", description="Weather forecast operations")

response_model, historical_response_model = register_models(ns)


# @ns.route("/predict")
# class PredictResource(Resource):
#     @ns.doc("get_temperature_forecast")
#     @ns.marshal_with(response_model)
#     def get(self):
#         try:
#             scaler = load_scaler()
#             data_normalized = load_normalized_data()
#             last_sequence = data_normalized[-cfg.N_HOURS :]
#             last_sequence = last_sequence.reshape(1, cfg.N_HOURS, -1)
#             last_sequence = data_normalized[-cfg.N_HOURS :]
#             last_sequence = last_sequence.reshape(1, cfg.N_HOURS, -1)

#             predicted_temps = recursive_forecast(last_sequence)
#             # dummy_data = np.zeros((len(predicted_temps), cfg.N_FEATURES))
#             # dummy_data[:, 0] = predicted_temps
#             # predicted_temps = scaler.inverse_transform(dummy_data)[:, 0]

#             last_known_features = data_normalized[-1, 1:]
#             repeated_features = np.tile(last_known_features, (len(predicted_temps), 1))
#             inv_input = np.concatenate(
#                 (predicted_temps.reshape(-1, 1), repeated_features), axis=1
#             )
#             predicted_temps = scaler.inverse_transform(inv_input)[:, 0]

#             next_times = get_next_hours()
#             response = {
#                 "status": 200,
#                 "message": "Success",
#                 "predictions": [
#                     {
#                         "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
#                         "temperature": round(float(temp), 2),
#                     }
#                     for time, temp in zip(next_times, predicted_temps)
#                 ],
#             }
#             return response
#         except Exception as e:
#             return {
#                 "status": 500,
#                 "message": f"Error: {str(e)}",
#                 "predictions": [],
#             }, 500


@ns.route("/predict/sarima")
class SARIMAPredictResource(Resource):
    @ns.doc("get_temperature_forecast_using_sarima")
    @ns.marshal_with(response_model)
    def get(self):
        try:
            predicted_df = pd.read_csv("/model/sarima/sarima_forecast_reversed.csv")
            
            if "ds" not in predicted_df or "temp" not in predicted_df:
                return {
                    "status": 400,
                    "message": "Missing required columns in the forecast data",
                    "predictions": [],
                }, 400
            

            response = {
                "status": 200,
                "message": "Success",
                "predictions": [
                    {"datetime": timestamp, "temperature": round(float(temp), 2)}
                    for timestamp, temp in zip(predicted_df["ds"], predicted_df["temp"])
                ],
            }
            return response
        except Exception as e:
            return {
                "status": 500,
                "message": f"Error: {str(e)}",
                "predictions": [],
            }, 500

@ns.route("/predict/dlinear")
class SARIMAPredictResource(Resource):
    @ns.doc("get_temperature_forecast_using_dlinear")
    @ns.marshal_with(response_model)
    def get(self):
        try:
            predicted_df = pd.read_csv("/model/dlinear/dlinear_forecast_reversed.csv")
            
            if "ds" not in predicted_df or "temp" not in predicted_df:
                return {
                    "status": 400,
                    "message": "Missing required columns in the forecast data",
                    "predictions": [],
                }, 400
            

            response = {
                "status": 200,
                "message": "Success",
                "predictions": [
                    {"datetime": timestamp, "temperature": round(float(temp), 2)}
                    for timestamp, temp in zip(predicted_df["ds"], predicted_df["temp"])
                ],
            }
            return response
        except Exception as e:
            return {
                "status": 500,
                "message": f"Error: {str(e)}",
                "predictions": [],
            }, 500


@ns.route("/historical")
class HistoricalResource(Resource):
    @ns.doc(params={
        "date": "Optional specific date to get data",
        "month": "Optional specific month to get data",
        "year": "Specific year to get data",
        "hour": "Optional specific hour to get data (HH)"
    })
    @ns.marshal_with(historical_response_model)
    def get(self):
        try:
            df_historical_data = load_historical_data()

            hour_str = request.args.get("hour")
            date_str = request.args.get("date")
            month_str = request.args.get("month")
            year_str = request.args.get("year")

            if not year_str:
                return {
                    "status": 400,
                    "message": "The 'year' parameter is required.",
                    "data": [],
                }, 400


            year = int(year_str)
            month = int(month_str) if month_str else None
            day = int(date_str) if date_str else None
            hour = int(hour_str) if hour_str else None


            mask = df_historical_data.index.year == year
            if month:
                mask &= df_historical_data.index.month == month
            if day:
                mask &= df_historical_data.index.day == day
            if hour:
                print(hour, flush=True)
                mask &= df_historical_data.index.hour == hour              

            df_filtered = df_historical_data[mask]
            if df_filtered.empty:
                return {
                    "status": 404,
                    "message": f"No data found",
                    "data": [],
                }, 404

            result = []
            for index, row in df_filtered.iterrows():
                item = {
                    "datetime": index.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": round(float(row["Temp"]), 2),
                    "rain": round(float(row.get("Rain", 0)), 2),
                    "cloud": round(float(row.get("Cloud", 0)), 2),
                    "pressure": round(float(row.get("Pressure", 0)), 2),
                    "wind": round(float(row.get("Wind", 0)), 2),
                    # "gust": round(float(row.get("Gust", 0)), 2),
                }
                result.append(item)

            return {"status": 200, "message": "Success", "data": result}
        except Exception as e:
            return {
                "status": 500,
                "message": f"Server error: {str(e)}",
                "data": [],
            }, 500
