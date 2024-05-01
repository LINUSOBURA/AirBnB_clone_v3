#!/usr/bin/python3
"""
v1 module for the api
"""

import os

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, origins=['0.0.0.0'])


@app.teardown_appcontext
def teardown_views(exception):
    """Close method to close views"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
