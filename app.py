import random
from uuid import UUID

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/car/<car_uuid>")
def car(car_uuid):
    return jsonify({
        'uuid': str(UUID(car_uuid)),
        'lat': random.uniform(-90, 90),
        'lon': random.uniform(-180, 180),
    })
