#!/usr/bin/python3
"""
All of the routes for state resource
"""
from api.v1.views import states
from flask import jsonify, abort, request
from models import storage
from models.state import State


@states.route("/", methods=['GET'])
def all_states():
    """Route to get all of the states"""
    states = storage.all("State").values()
    all_states = []
    for state in states:
        dict_form = state.to_dict()
        all_states.append(dict_form)
    return jsonify(all_states)


@states.route("/<string:state_id>", methods=['GET'])
def get_state_wtith_id(state_id):
    """Get state with a particular ID"""
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            matching_state = state.to_dict()
            return jsonify(matching_state)
    abort(404)


@states.route("/<string:state_id>", methods=['DELETE'])
def delete_state_with_id(state_id):
    """Deletes a state with a particular ID"""
    states = storage.all("State").values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@states.route("/", methods=['POST'])
def create_state():
    """Create a new state"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new_state = request.get_json()
    if new_state.get("name") is None:
        abort(400, "Missing name")
    state_obj = State(**new_state)
    storage.new(state_obj)
    storage.save()
    storage.close()
    return jsonify(state_obj.to_dict()), 201


@states.route("/<string:state_id>", methods=['PUT'])
def update_state_with_id(state_id):
    """Updates a state with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_state = storage.get("State", state_id)
    forbidden_keys = ["id", "created_at", "updated_at"]
    if matching_state:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_state, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_state.to_dict())
    abort(404)
