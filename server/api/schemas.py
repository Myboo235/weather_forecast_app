from flask_restx import fields


def register_models(api):
    prediction_model = api.model(
        "Prediction",
        {
            "datetime": fields.String(required=True),
            "temperature": fields.Float(required=True),
        },
    )

    response_model = api.model(
        "PredictionResponse",
        {
            "status": fields.Integer,
            "message": fields.String,
            "predictions": fields.List(fields.Nested(prediction_model)),
        },
    )

    historical_data_model = api.model(
        "HistoricalData",
        {
            "datetime": fields.String,
            "temperature": fields.Float,
            "rain": fields.Float,
            "cloud": fields.Float,
            "pressure": fields.Float,
            "wind": fields.Float,
            # 'gust': fields.Float
        },
    )

    historical_response_model = api.model(
        "HistoricalResponse",
        {
            "status": fields.Integer,
            "message": fields.String,
            "data": fields.List(fields.Nested(historical_data_model)),
        },
    )

    metrics_model = api.model(
        "MetricsResource",
        {
            "rmse": fields.Float,
            "mse": fields.Float,
            "mae": fields.Float,
            "horizon": fields.Integer,
            "model": fields.String,
        },
    )

    metrics_response_model = api.model(
        "MetricsResponse",
        {
            "status": fields.Integer,
            "message": fields.String,
            "metrics": fields.Nested(metrics_model),
        },
    )

    return response_model, historical_response_model, metrics_response_model
