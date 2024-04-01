#!/usr/bin/python3
""" The cities route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ returns the list of all cities """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])
    elif request.method == 'POST':
        create = request.get_json()
        if create is None or type(create) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif create.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        created_city = City(state_id=state_id, **create)
        created_city.save()
        return jsonify(created_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    """ Retrieves a City object with the provided id """
    city = storage.get('City', city_id)

    if city is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city = storage.get('City', city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                storage.save()

        return jsonify(city.to_dict()), 200
