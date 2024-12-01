from http import HTTPStatus
from flask import Flask, jsonify
from flasgger import Swagger

from dotenv import load_dotenv

load_dotenv()

from adapters.http import order_api

app = Flask("FoodAPI")
swagger = Swagger(app)

BASE_PATH = "/api/v1"

app.register_blueprint(order_api, url_prefix=BASE_PATH)


app.json.sort_keys = False


@app.get("/")
def root():
    return jsonify({"project": "Tech Challence - Fase 4"}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
