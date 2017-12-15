#!/usr/bin/python3
"""
All of the routes for amenity resource
"""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.amenity import Amenity

amenities = Blueprint("amenities", __name__)


@amenities.route("/", methods=['GET'])
def all_amenity():
    """Route to get all of the amenity"""
    amenity = storage.all("Amenity").values()
    all_amenity = []
    for amenity in amenity:
        dict_form = amenity.to_dict()
        all_amenity.append(dict_form)
    return jsonify(all_amenity)


@amenities.route("/<string:amenity_id>", methods=['GET'])
def get_amenity_with_id(amenity_id):
    """Get amenity with a particular ID"""
    amenity = storage.all("Amenity").values()
    for amenity in amenity:
        if amenity.id == amenity_id:
            matching_amenity = amenity.to_dict()
            return jsonify(matching_amenity)
    abort(404)


@amenities.route("/<string:amenity_id>", methods=['DELETE'])
def delete_amenity_with_id(amenity_id):
    """Deletes a amenity with a particular ID"""
    amenity = storage.all("Amenity").values()
    for amenity in amenity:
        if amenity.id == amenity_id:
            storage.delete(amenity)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@amenities.route("/", methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new_amenity = request.get_json()
    if new_amenity.get("name") is None:
        abort(400, "Missing name")
    amenity_obj = Amenity(**new_amenity)
    storage.new(amenity_obj)
    storage.save()
    storage.close()
    return jsonify(amenity_obj.to_dict()), 201


@amenities.route("/<string:amenity_id>", methods=['PUT'])
def update_amenity_with_id(amenity_id):
    """Updates a amenity with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_amenity = storage.get("Amenity", amenity_id)
    forbidden_keys = ["id", "created_at", "updated_at"]
    if matching_amenity:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_amenity, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_amenity.to_dict())
    abort(404)
