import os
import uuid
from logging.config import dictConfig

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
DB_URL = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Car(db.Model):
    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/car/<car_uuid>", methods=['GET', 'PUT'])
def car(car_uuid):
    app.logger.info("Received request to %s car information for car '%s'", request.method, car_uuid)
    if request.method == 'GET':
        app.logger.debug("Querying DB for car with uuid=%s", car_uuid)
        obj = Car.query.get(uuid.UUID(car_uuid))
        if not obj:
            abort(404)
        app.logger.debug("Found a matching car for %s with coordinates: lat=%f lon=%f", car_uuid, obj.lat, obj.lon)
        return jsonify({
            'uuid': str(obj.uuid),
            'lat': obj.lat,
            'lon': obj.lon,
        })
    elif request.method == 'PUT':
        car_info = request.get_json()
        obj = Car(uuid=uuid.UUID(car_uuid), lat=car_info['lat'], lon=car_info['lon'])
        db.session.merge(obj)
        db.session.commit()
        return 'OK'


@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""
    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)
    print('Creating tables.')
    db.create_all()
    print('Shiny!')
