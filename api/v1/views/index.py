#!/usr/bin/python3

""" The status route """

from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ returns the status of the route """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def get_stats():
    """ retrieves the number of each object by type """
    objects = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    for key, value in object.items():
        objects[key] = storage.count(value)

    return jsonify(objects)
