#!/usr/bin/python3
""" The users route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """ returns the list of all users """
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in storage.all('User')
                        .values()])
    elif request.method == 'POST':
        create = request.get_json()
        if create is None or type(create) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif create.get('email') is None:
            return jsonify({'error': 'Missing email'}), 400
        elif create.get('password') is None:
            return jsonify({'error': 'Missing password'}), 400
        created_user = User(**create)
        created_user.save()
        return jsonify(created_user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_by_id(user_id):
    """ Retrieves a User object with the provided id """
    user = storage.get('User', user_id)

    if user is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        user = storage.get('User', user_id)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
                storage.save()

        return jsonify(user.to_dict()), 200
