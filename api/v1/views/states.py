#!/usr/bin/python3
"""Module for CRUD of states"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Get all the states"""
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 'OK'


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), '200'


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    if not request.json:
        abort(400, {"Not a JSON"})
    if 'name' not in request.json:
        abort(400, {"Missing name"})
    data = request.json
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update and existing state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, {"Not a JSON"})
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), '200'
