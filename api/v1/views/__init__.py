#!/usr/bin/python3
"""
App Views Blueprint
"""
from flask import Blueprint
import json

app_views = Blueprint("app_views", __name__)

from api.v1.views.index import *
