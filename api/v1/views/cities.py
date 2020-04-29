#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """ Return all cities """
    all_cities = []
    for my_cities in storage.all('City').values():
        all_cities.append(my_cities.to_dict())
    return jsonify(all_cities), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Return cities for ID states """
    my_cities = storage.get('State', state_id)
    if my_cities is None:
        abort(404)
    else:
        data = my_cities.to_dict()
        return jsonify(data)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_list_id(city_id):
    """ Return cities for ID"""
    my_city = storage.get('City', city_id)
    if my_city:
        return jsonify(my_city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def cities_remove(city_id):
    """ Delete cities for ID """
    my_cities = storage.get('City', city_id)
    if my_cities:
        storage.delete(my_cities)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_cities(state_id):
    """ Create Cities """
    my_cities = request.get_json()
    if not my_cities:
        return 'Not a JSON', 400
    if 'name' not in my_cities:
        return "Missing name", 400
    if not storage.get('State', state_id):
        abort(404)
    else:
        city = City(**my_cities)
        setattr(city, 'state_id', state_id)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """ Update cities using put """
    my_cities = request.get_json()
    if not my_cities:
        return 'Not a JSON', 400
    else:
        upt_cities = storage.get("City", city_id)
        if upt_cities is None:
            abort(404)
        else:
            for attr in my_cities:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at" or attr == 'state_id':
                    continue
                setattr(upt_cities, attr, my_cities[attr])
            storage.save()
            return jsonify(upt_cities.to_dict()), 200
