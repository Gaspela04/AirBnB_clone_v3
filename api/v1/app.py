#!/usr/bin/python3
"""Api hbnb"""
from api.v1.views import app_views
from models import storage
from flask import Flask
from flask import Flask, Blueprint, jsonify

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def strg_close(x):
    """Close session storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)
