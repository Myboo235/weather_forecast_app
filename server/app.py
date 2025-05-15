from flask import Flask, redirect, send_from_directory
from flask_restx import Api, Resource
from api.routes import ns as weather_ns
from flask_cors import CORS

app = Flask(
    __name__,
    static_folder="/ui",        # Folder for static frontend files
    static_url_path=""         # Serve static files at root "/"
)
app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
app.config['RESTX_MASK_SWAGGER'] = False
CORS(app)

api = Api(
    app,
    version="1.0",
    title="Weather Forecast API",
    description="API for weather forecasting using LSTM model",
    doc="/api-docs",
)

api.add_namespace(weather_ns, path="/api")

@api.route("/home")
class HomeResource(Resource):
    def get(self):
        return send_from_directory(app.static_folder, "index.html")


@app.errorhandler(404)
def not_found(e):
    return redirect("/home")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
