#!/usr/bin/python3
"""index file"""
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """ Return status OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ retrieve the number of each object by type """
    return jsonify(states=storage.count(State))
