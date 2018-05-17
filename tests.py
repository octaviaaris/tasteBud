import unittest

from server import app
from model import db, connect_to_db

class DatabaseTests(unittest.TestCase):
	"""Tests database-related functionality."""

	def setUp(self):
		"""Run before every test."""

		pass

	def tearDown(self):
		"""Run at the end of every test."""

		pass

class UnitTests(unittest.TestCase):
	"""Test functions."""

	def setUp(self):
		"""Run before every test."""

		pass

	def tearDown(self):
		"""Run at the end of every test."""

		pass

class FlaskTests(unittest.TestCase):

	def setUp(self):
		"""Run before every test."""

		self.client = app.test_client()
		app.config['TESTING'] = True

	def tearDown(self):
		"""Run at the end of every test."""

		pass

	def test_root_route(self):
		"""Test root."""

		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn()