#!/usr/bin/python3
""" The Reviews route """

from flask import jsonify, Blueprint, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """ returns the list of all reviews """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.reviews])
    elif request.method == 'POST':
        create = request.get_json()
        if create is None or type(create) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        elif create.get('user_id') is None:
            return jsonify({'error': 'Missing user_id'})
        elif storage.get('User', create.get('user_id')) is None:
            abort(404)
        elif create.get('text') is None:
            return jsonify({'error': 'Missing text'}), 400

        created_review = Review(place_id=place_id, **create)
        created_review.save()
        return jsonify(created_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review_by_id(review_id):
    """ Retrieves a Review object with the provided id """
    review = storage.get('Review', review_id)

    if review is None:
        abort(404)
    elif request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        review = storage.get('Review', review_id)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        update = request.get_json()
        if update is None or type(update) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        for key, value in update.items():
            if key not in ['id', 'user_id', 'created_at', 'updated_at',
                           'place_id']:
                setattr(review, key, value)
                storage.save()

        return jsonify(review.to_dict()), 200
