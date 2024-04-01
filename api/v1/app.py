#!/usr/bin/python3

""" flask API status """

from os import getenv
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(error):
    """ closes a db session """
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True,
            debug=True)
