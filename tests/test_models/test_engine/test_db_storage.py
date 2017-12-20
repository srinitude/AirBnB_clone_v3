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
import models

if models.storage == "db":
        classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

        class TestDBStorage(unittest.TestCase):
	    """ tests for db storage """
            def setUp(self):
                self.session = db_storage.DBStorage()
                self.session.reload()

	    def tearDown(self):
		self.session.close()

	    def test_get_returns_none(self):
		"""Test that get with nothing in it properly returns None"""
		result = self.session.get("User", "234htnfjkegr42--23q524yhwgeasgset")
		self.assertEqual(result, None)

	    def test_count_returns_none(self):
		"""Test that count with nothing in it properly returns 0"""
		result = self.session.count("BadClass")
		self.assertEqual(result, 0)

	    def test_valid_get(self):
		"""Tests valid get"""
		new_state = State(name="Montana")
		self.session.new(new_state)
		state_result = self.session.get("State", new_state.id)
		self.assertEqual(id(new_state), id(state_result))
		self.session.delete(new_state)

	    def test_valid_count(self):
		"""Tests valid count"""
		current_count = self.session.count("State")
		new_state = State(name="Montana")
		self.session.new(new_state)
		new_count = self.session.count("State")
		self.assertEqual(current_count + 1, new_count)
		self.session.delete(new_state)
