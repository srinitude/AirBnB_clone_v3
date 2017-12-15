#!/usr/bin/python3
"""
All of the routes for city resource
"""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.place import Place

cities = Blueprint("cities", __name__)


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


@cities.route("/<string:city_id>/places", methods=['GET'])
def all_places(city_id):
    """Route to get all of the place"""
    places = storage.all("Place").values()
    all_place = []
    matching_city = storage.get("City", city_id)
    if matching_city:
        for place in places:
            dict_form = place.to_dict()
            all_place.append(dict_form)
        return jsonify(all_place)
    abort(404)


@cities.route("/<string:city_id>/places", methods=['POST'])
def create_place(city_id):
    """Create a new place"""
    if not storage.get("City", city_id):
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    new_place = request.get_json()
    if new_place.get("user_id") is None:
        abort(400, "Missing user_id")
    user_id = new_place.get("user_id")
    if not storage.get("User", user_id):
        abort(404)
    if new_place.get("name") is None:
        abort(400, "Missing name")
    matching_city = storage.get("City", city_id)
    matching_user = storage.get("User", user_id)
    if matching_city and matching_user:
        for key, val in new_place.items():
                setattr(matching_city, key, val)
        place_obj = Place(**new_place)
        storage.new(place_obj)
        storage.save()
        storage.close()
        return jsonify(place_obj.to_dict()), 201
    abort(404)
