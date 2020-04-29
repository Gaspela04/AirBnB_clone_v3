#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Return all amenities """
    all_amenities = []
    for my_amenities in storage.all('Amenity').values():
        all_amenities.append(my_amenities.to_dict())
    return jsonify(all_amenities), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id):
    """ Return amenities for ID"""
    my_amenity = storage.get("Amenity", amenity_id)
    if my_amenity:
        return jsonify(my_amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenities(amenity_id):
    """ Delete amenities for ID """
    my_amenities = storage.get("Amenity", amenity_id)
    if my_amenities:
        storage.delete(my_amenities)
        storage.save()
        storage.close()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """ Create Amenities """
    my_amenities = request.get_json()
    if not my_amenities:
        return 'Not a JSON', 400
    if 'name' not in my_amenities:
        return "Missing name", 400
    else:
        amenity = Amenity(**my_amenities)
        storage.new(amenity)
        storage.save()
        storage.close()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ Update cities using put """
    my_amenities = request.get_json()
    if not my_amenities:
        return 'Not a JSON', 400
    if 'name' not in my_amenities:
        return "Missing name", 400
    else:
        upt_amenities = storage.get("Amenity", amenity_id)
        if upt_amenities is None:
            abort(404)
        else:
            for attr in my_amenities:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at":
                    continue
                setattr(upt_amenities, attr, my_amenities[attr])
            storage.save()
            storage.close()
            return jsonify(upt_amenities.to_dict()), 200
