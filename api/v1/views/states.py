#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Return all states """
    all_state = []
    for my_state in storage.all(State).values():
        all_state.append(my_state.to_dict())
    return jsonify(all_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Return states for ID """
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)
    else:
        ret = my_state.to_dict()
        return jsonify(ret)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete states for ID """
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)
    else:
        storage.delete(my_state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create States """
    my_state = request.get_json()
    if my_state is None:
        abort(make_response("Not a JSON", 400))
    else:
        if "name" not in my_state.keys():
            abort(make_response("Missing name", 400))
        else:
            add_state = State(**my_state)
            storage.new(add_state)
            add_state.save()
            return jsonify(add_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update states using put """
    my_state = storage.get("State", state_id)
    if my_state is None:
        abort(404)
    else:
        update_state = request.get_json()
        add_key = set(('id', 'created_at', 'updated_at'))
        if update_state is None:
            abort(make_response("Not a JSON", 400))
        getdict = {key: value for key, value in update_state.items()
                   if key not in add_key}
        for key, value in getdict.items():
            setattr(my_state, key, value)
        storage.save()
        return jsonify(my_state.to_dict()), 200
