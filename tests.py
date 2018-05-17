import unittest

from server import app
from model import db, connect_to_db, example_users, example_ratings
from seed import *

class DatabaseTests(unittest.TestCase):
	"""Tests database-related functionality."""

	def setUp(self):
		"""Run before every test."""

		# connect to test database
		connect_to_db(app, "postgresql:///testdb")

		# create tables and add sample data
		db.create_all()

		# seed testdb
		seed_prices()
		seed_categories('database/categories.txt')
		seed_restaurants('database/all_restaurants.txt')
		seed_price_ratings('database/price_ratings.txt')
		seed_rest_cats('database/all_restaurants.txt')
		seed_users('database/users.csv')
		seed_ratings('database/ratings.csv')
		
		# create test users and ratings
		example_users()
		example_ratings()

	def tearDown(self):
		"""Run at the end of every test."""

		db.session.close()
		db.drop_all()

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

	def test_root(self):
		"""Test root route."""

		result = self.client.get("/")
		self.assertEqual(result.status_code, 200)
		self.assertIn('Log In', result.data)
		self.assertIn('Sign Up', result.data)
		self.assertNotIn('Back to profile', result.data)

	def test_login(self):
		"""Test login route."""

		result = self.client.get("/login")
		self.assertEqual(result.status_code, 200)
		self.assertIn('Back to profile', result.data)
		self.assertIn('Log In', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_login(self):
	"""Test handle-login route."""

		result = self.client.post("/handle-login",
								  data={'username': 'opi',
								  		'password': 'opi'},
								  follow_redirects=True)

		self.assertEqual(result.status_code, 200)
		self.assertIn('Back to profile', result.data)
		self.assertIn('Log In', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_logout(self):
	"""Test handle-logout route."""

		pass

	def test_signup(self):
	"""Test signup route."""

		pass

	def test_handle_signup(self):
	"""Test handle-signup route."""

		pass

	def test_profile(self):
	"""Test profile route."""

		pass

	def test_search(self):
	"""Test search route."""

		pass

	def test_search_results(self):
	"""Test search-results route."""

		pass

	def test_details(self):
	"""Test details route."""

		pass

	def test_rate_restaurant(self):
	"""Test rate-restaurant route."""

		pass
























if __name__ == "__main__":
	unittest.main()