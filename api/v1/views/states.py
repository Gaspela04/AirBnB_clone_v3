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
    for my_state in storage.all("State").values():
        all_state.append(my_state.to_dict())
    return jsonify(all_state), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Return states for ID """
    my_state = storage.get("State", state_id)
    if my_state:
        return jsonify(my_state.to_dict()), 200
    else:
        abort(404)


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Delete states for ID """
    my_state = storage.get("State", state_id)
    if my_state:
        storage.delete(my_state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create States """
    my_state = request.get_json()
    if not my_state:
        return 'Not a JSON', 400
    if 'name' not in my_state:
        return "Missing name", 400
    else:
        state = State(**my_state)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update states using put """
    my_state = request.get_json()
    if not my_state:
        return 'Not a JSON', 400
    else:
        upd_state = storage.get("State", state_id)
        if upd_state is None:
            abort(404)
        else:
            for attr in my_state:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at":
                    continue
                setattr(upd_state, attr, my_state[attr])
            storage.save()
            return jsonify(upd_state.to_dict()), 200
