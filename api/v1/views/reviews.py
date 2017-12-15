#!/usr/bin/python3
"""
All of the routes for review resource
"""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.review import Review

reviews = Blueprint("reviews", __name__)


@reviews.route("/<string:review_id>", methods=['GET'])
def get_review_with_id(review_id):
    """Get review with a particular ID"""
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.id == review_id:
            matching_review = review.to_dict()
            return jsonify(matching_review)
    abort(404)


@reviews.route("/<string:review_id>", methods=['DELETE'])
def delete_review_with_id(review_id):
    """Deletes a review with a particular ID"""
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@reviews.route("/<string:review_id>", methods=['PUT'])
def update_review_with_id(review_id):
    """Updates a review with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_review = storage.get("Review", review_id)
    forbidden_keys = ["id", "created_at", "updated_at", "user_id", "place_id"]
    if matching_review:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_review, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_review.to_dict())
    abort(404)
