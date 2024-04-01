#!/usr/bin/python3
""" The states route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """ returns the list of all states """
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in storage.all('State')
                        .values()])
    elif request.method == 'POST':
        state = request.get_json()
        if state is None or type(state) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif state.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        created_state = State(**state)
        created_state.save()
        return jsonify(created_state.to_dict()), 201


@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states_by_id(state_id):
    """ Retrieves a State object with the provided id """
    state = storage.get('State', state_id)

    if state is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state = storage.get('State', state_id)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
                storage.save()

        return jsonify(state.to_dict()), 200
