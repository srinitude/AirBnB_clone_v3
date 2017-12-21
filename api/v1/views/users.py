#!/usr/bin/python3
"""
All of the routes for user resource
"""
from flask import jsonify, abort, request, Blueprint
from models import storage
from models.user import User

users = Blueprint("users", __name__)


@users.route("/", methods=['GET'])
def all_users():
    """Route to get all of the users"""
    users = storage.all("User").values()
    all_users = []
    for user in users:
        dict_form = user.to_dict()
        all_users.append(dict_form)
    return jsonify(all_users)


@users.route("/<string:user_id>", methods=['GET'])
def get_user_with_id(user_id):
    """Get user with a particular ID"""
    users = storage.all("User").values()
    for user in users:
        if user.id == user_id:
            matching_user = user.to_dict()
            return jsonify(matching_user)
    abort(404)


@users.route("/<string:user_id>", methods=['DELETE'])
def delete_user_with_id(user_id):
    """Deletes a user with a particular ID"""
    users = storage.all("User").values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@users.route("/", methods=['POST'])
def create_user():
    """Create a new user"""
    if not request.is_json:
        abort(400, "Not a JSON")
    new_user = request.get_json()
    if new_user.get("email") is None:
        abort(400, "Missing email")
    if new_user.get("password") is None:
        abort(400, "Missing password")
    user_obj = User(**new_user)
    storage.new(user_obj)
    storage.save()
    storage.close()
    return jsonify(user_obj.to_dict()), 201


@users.route("/<string:user_id>", methods=['PUT'])
def update_user_with_id(user_id):
    """Updates a user with a particular ID"""
    if not request.is_json:
        abort(400, "Not a JSON")
    dict_updates = request.get_json()
    matching_user = storage.get("User", user_id)
    forbidden_keys = ["id", "created_at", "updated_at"]
    if matching_user:
        for key, val in dict_updates.items():
            if key not in forbidden_keys:
                setattr(matching_user, key, val)
        storage.save()
        storage.close()
        return jsonify(matching_user.to_dict())
    abort(404)
