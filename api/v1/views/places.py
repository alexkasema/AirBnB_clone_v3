#!/usr/bin/python3
""" The places route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """ returns the list of all places """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])
    elif request.method == 'POST':
        create = request.get_json()
        if create is None or type(create) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif create.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'})
        elif storage.get('User', create.get('user_id')) is None:
            abort(404)
        elif create.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        created_place = Place(city_id=city_id, **create)
        created_place.save()
        return jsonify(created_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):
    """ Retrieves a Place object with the provided id """
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place = storage.get('Place', place_id)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at',
                           'city_id']:
                setattr(place, key, value)
                storage.save()

        return jsonify(place.to_dict()), 200
