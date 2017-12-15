#!/usr/bin/python3
"""
All of the routes for city resource
"""
from api.v1.views import cities
from flask import jsonify, abort, request
from models import storage
from models.city import City


@cities.route("/<string:city_id>", methods=['GET'])
def get_city_with_id(city_id):
    """Get city with a particular ID"""
    cities = storage.all("City").values()
    for city in cities:
        if city.id == city_id:
            matching_city = city.to_dict()
            return jsonify(matching_city)
    abort(404)


@cities.route("/<string:city_id>", methods=['DELETE'])
def delete_city_with_id(city_id):
    """Deletes a city with a particular ID"""
    cities = storage.all("City").values()
    for city in cities:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@cities.route("/<string:city_id>", methods=['PUT'])
def update_city_with_id(city_id):
    """Updates a city with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_city = storage.get("City", city_id)
    forbidden_keys = ["id", "created_at", "updated_at"]
    if matching_city:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_city, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_city.to_dict())
    abort(404)
