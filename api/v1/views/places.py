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
    forbidden_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    if matching_place:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_place, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_place.to_dict())
    abort(404)


@places.route("/<string:place_id>/reviews", methods=['GET'])
def all_review(place_id):
    """Route to get all of the review"""
    reviews = storage.all("Review").values()
    all_review = []
    matching_place = storage.get("Place", place_id)
    if matching_place:
        for review in reviews:
            if review.place_id == place_id:
                dict_form = review.to_dict()
                all_review.append(dict_form)
        return jsonify(all_review)
    abort(404)


@places.route("/<string:place_id>/reviews", methods=['POST'])
def create_review(place_id):
    """Create a new review"""
    if not storage.get("Place", place_id):
        abort(404)
    if not request.is_json:
        abort(400, "Not a JSON")
    new_review = request.get_json()
    if new_review.get("user_id") is None:
        abort(400, "Missing user_id")
    user_id = new_review.get("user_id")
    if not storage.get("User", user_id):
        abort(404)
    if new_review.get("text") is None:
        abort(400, "Missing text")
    matching_place = storage.get("Place", place_id)
    matching_user = storage.get("User", user_id)
    if matching_place and matching_user:
        for key, val in new_review.items():
                setattr(matching_user, key, val)
        new_review["place_id"] = place_id
        review_obj = Place(**new_review)
        storage.new(review_obj)
        storage.save()
        storage.close()
        return jsonify(review_obj.to_dict()), 201
