#!/usr/bin/python3
""" Rest API """
from flask import Flask, request
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """ Return all cities """
    all_cities = []
    for my_cities in storage.all('City').values():
        all_cities.append(my_cities.to_dict())
    return jsonify(all_cities)


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
        return my_city.to_dict()
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def cities_remove(city_id):
    """ Delete cities for ID """
    my_cities = storage.get('City', city_id)
    if my_cities is None:
        abort(404)
    else:
        storage.delete(my_cities)
        storage.save()
        return jsonify({}), 200
