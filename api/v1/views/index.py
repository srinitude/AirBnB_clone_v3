#!/usr/bin/python3
"""
App views
"""
from api.v1.views import *
from flask import jsonify, Blueprint
from models import storage

app_views = Blueprint("app_views", __name__)


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def number_of_objects():
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places":  storage.count("Place"),
        "reviews":  storage.count("Review"),
        "states":  storage.count("State"),
        "users": storage.count("User")
        })
