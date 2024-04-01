#!/usr/bin/python3
""" The amenities route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """ returns the list of all amenities """
    if request.method == 'GET':
        return jsonify([amenity.to_dict() for amenity in storage.all('Amenity')
                        .values()])
    elif request.method == 'POST':
        create = request.get_json()
        if create is None or type(create) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif create.get('name') is None:
            return jsonify({'error': 'Missing name'}), 400

        created_amenity = Amenity(**create)
        created_amenity.save()
        return jsonify(created_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities_by_id(amenity_id):
    """ Retrieves an Amenity object with the provided id """
    amenity = storage.get('Amenity', amenity_id)

    if amenity is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity = storage.get('Amenity', amenity_id)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
                storage.save()

        return jsonify(amenity.to_dict()), 200
