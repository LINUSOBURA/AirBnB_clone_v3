#!/usr/bin/python3
"""App views module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats_get():
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    stats_dict = {}
    for cls, route in classes.items():
        stats_dict[route] = storage.count(cls)
    return jsonify(stats_dict)
