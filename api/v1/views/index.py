#!/usr/bin/python3
"""index file"""
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return a JSON """
    return {"status": "OK"}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ retrieve the number of each object by type """
    return {"amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')}
