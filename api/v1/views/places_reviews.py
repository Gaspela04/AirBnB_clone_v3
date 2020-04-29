#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def all_reviews(place_id):
    """ Return reviews for ID places """
    all_reviews = storage.get("Place", place_id)
    if not all_reviews:
        abort(404)
    else:
        review_list = []
        for review in all_reviews.reviews:
            review_list.append(review.to_dict())
    return jsonify(review_list), 200


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_reviews(review_id):
    """ Return reviews for ID"""
    my_review = storage.get("Review", review_id)
    if my_review:
        return jsonify(my_review.to_dict()), 200
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    """ Delete reviews for ID """
    my_reviews = storage.get("Review", review_id)
    if my_reviews:
        storage.delete(my_reviews)
        storage.save()
        storage.close()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Create reviews """
    my_reviews = request.get_json()
    if not my_reviews:
        return 'Not a JSON', 400
    if 'user_id' not in my_reviews:
        return "Missing user_id", 400
    if not storage.get('User', my_reviews.get('user_id')):
        abort(404)
    if 'text' not in my_reviews:
        return 'Missing text', 400
    if not storage.get('Place', place_id):
        abort(404)
    else:
        review = Review(**my_reviews)
        setattr(review, 'place_id', place_id)
        storage.new(review)
        storage.save()
        storage.close()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """ Update reviews using put """
    my_reviews = request.get_json()
    if not my_reviews:
        return 'Not a JSON', 400
    else:
        upt_reviews = storage.get("Review", review_id)
        if upt_reviews is None:
            abort(404)
        else:
            for attr in my_reviews:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at" or attr == 'user_id' or \
                        attr == 'place_id':
                    continue
                setattr(upt_reviews, attr, my_reviews[attr])
            storage.save()
            storage.close()
            return jsonify(upt_reviews.to_dict()), 200
