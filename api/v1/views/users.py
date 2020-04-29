#!/usr/bin/python3
""" Rest API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Return all users """
    all_users = []
    for my_users in storage.all('User').values():
        all_users.append(my_users.to_dict())
    return jsonify(all_users), 200


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_users(user_id):
    """ Return users for ID"""
    my_user = storage.get("User", user_id)
    if my_user:
        return jsonify(my_user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_users(amenuser_idity_id):
    """ Delete users for ID """
    my_users = storage.get("User", user_id)
    if my_users:
        storage.delete(my_users)
        storage.save()
        storage.close()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """ Create users """
    my_users = request.get_json()
    if not my_users:
        return 'Not a JSON', 400
    if 'email' not in my_users:
        return "Missing email", 400
    if 'password' not in my_users:
        return 'Missing password', 400
    else:
        user = User(**my_users)
        storage.new(user)
        storage.save()
        storage.close()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """ Update users using put """
    my_users = request.get_json()
    if not my_users:
        return 'Not a JSON', 400
    else:
        upt_users = storage.get("User", user_id)
        if upt_users is None:
            abort(404)
        else:
            for attr in my_users:
                if attr == "id" or attr == "created_at" or \
                        attr == "updated_at" or attr == 'email':
                    continue
                setattr(upt_users, attr, my_users[attr])
            storage.save()
            storage.close()
            return jsonify(upt_users.to_dict()), 200
