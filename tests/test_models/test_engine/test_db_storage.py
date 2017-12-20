#!/usr/bin/python3
"""
Contains the TestDBStorage classes
"""

from datetime import datetime
import inspect
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import sqlalchemy
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestDBStorage(unittest.TestCase):
    """ tests for db storage """
    def setUp(self):
        self.session = db_storage.DBStorage()

    def tearDown(self):
        self.session.close()

    def test_get_returns_none(self):
        """Test that get with nothing in it properly returns None"""
        result = self.session.get("User", "234htnfjkegr42--23q524yhwgeasgset")
        self.assertEqual(result, None)

    def test_count_returns_none(self):
        """Test that count with nothing in it properly returns 0"""
        result = self.session.count()
        self.assertEqual(result, 0)

    def test_valid_get(self):
        """Tests valid get"""
        new_user = User()
        self.session.new(new_user)
        user_result = self.session.get("User", new_user.id)
        self.assertEqual(id(new_user), id(user_result))

    def test_valid_count(self):
        """Tests valid count"""
        new_user = User()
        self.session.new(new_user)
        count = self.session.count("User")
        self.assertEqual(count, 1)
