#!/usr/bin/python3
"""
All of the routes for place resource
"""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.place import Place

places = Blueprint("places", __name__)


@places.route("/<string:place_id>", methods=['GET'])
def get_place_with_id(place_id):
    """Get place with a particular ID"""
    places = storage.all("Place").values()
    for place in places:
        if place.id == place_id:
            matching_place = place.to_dict()
            return jsonify(matching_place)
    abort(404)


@places.route("/<string:place_id>", methods=['DELETE'])
def delete_place_with_id(place_id):
    """Deletes a place with a particular ID"""
    places = storage.all("Place").values()
    for place in places:
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@places.route("/<string:place_id>", methods=['PUT'])
def update_place_with_id(place_id):
    """Updates a place with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_place = storage.get("Place", place_id)
    forbidden_keys = ["id", "created_at", "updated_at"]
    if matching_place:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_place, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_place.to_dict())
    abort(404)
