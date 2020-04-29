#!/usr/bin/python3
"""Api hbnb"""
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def strg_close(x):
    """Close session storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error 404 """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
