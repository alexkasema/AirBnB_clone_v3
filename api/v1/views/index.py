#!/usr/bin/python3

""" The status route """

from flask import jsonify, Blueprint
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ returns the status of the route """
    return jsonify({"status": "OK"})
