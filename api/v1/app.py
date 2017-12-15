#!/usr/bin/python3
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close(f):
    """ app teardown """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ 404 alternate """
    return jsonify({"error": "Not found"})

if __name__ == '__main__':
    HBNB_HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    try:
        HBNB_PORT = int(os.getenv("HBNB_API_PORT"))
    except:
        HBNB_PORT = 5000
    app.run(host=HBNB_HOST, port=HBNB_PORT)
