#!/usr/bin/python3
"""Module for CRUD of states"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Get all the Places from a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get a place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a city by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), '200'


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new user"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), '201'


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update and existing City"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), '200'


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on JSON request body"""
    if not request.json:
        abort(400, "Not a JSON")

    states = request.json.get('states', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                places.extend(state.places)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = {amenity.id for amenity in place.amenities}
            if set(amenities).issubset(place_amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
