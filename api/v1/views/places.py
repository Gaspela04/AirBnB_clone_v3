#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def all_places():
    """ Return all states """
    all_place = []
    for my_place in storage.all('Place').values():
        all_place.append(my_place.to_dict())
    return jsonify(all_place), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Return places for ID cities """
    my_places = storage.get('City', city_id)
    if my_places:
        places = []
        for place in my_places.places:
            places.append(place.to_dict())
        return jsonify(places), 200
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def places_list_id(place_id):
    """ Return places for ID """
    my_place = storage.get("Place", place_id)
    if my_place:
        return jsonify(my_place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """ Delete palces for ID """
    my_places = storage.get("Place", place_id)
    if my_places:
        storage.delete(my_places)
        storage.save()
        storage.close()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_places(city_id):
    """ Create palces """
    my_places = request.get_json()
    if not my_places:
        return 'Not a JSON', 400
    if 'user_id' not in my_places:
        return "Missing user_id", 400
    if 'name' not in my_places:
        return 'Missing name', 400
    if not storage.get('User', my_places.get('user_id')):
        abort(404)
    if not storage.get('City', city_id):
        abort(404)
    else:
        place = Place(**my_places)
        setattr(place, 'city_id', city_id)
        storage.new(place)
        storage.save()
        storage.close()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """ Update cities using put """
    my_places = request.get_json()
    if not my_places:
        return 'Not a JSON', 400
    else:
        upt_places = storage.get("Place", place_id)
        if upt_places is None:
            abort(404)
        else:
            for attr in my_places:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at" or attr == 'user_id' or \
                        attr == 'city_id':
                    continue
                setattr(upt_places, attr, my_places[attr])
            storage.save()
            storage.close()
            return jsonify(upt_places.to_dict()), 200
