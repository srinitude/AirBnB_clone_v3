#!/usr/bin/python3
"""
App Views Blueprint
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)
states = Blueprint("states", __name__)
cities = Blueprint("cities", __name__)

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
