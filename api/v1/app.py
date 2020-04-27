#!/usr/bin/python3
"""Api hbnb"""
from models import storage
from flask import Flask

app = Flask(__name__)

from api.v1.views import app_views
app.register_blueprint(app_views)

@app.teardown_appcontext
def strg_close(x):
    """Close session storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", threaded=True)