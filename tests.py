import unittest

from server import app
from model import db, connect_to_db, example_users, example_ratings
from seed import (seed_prices,
				  seed_categories,
				  seed_restaurants,
				  seed_price_ratings,
				  seed_rest_cats,
				  seed_users,
				  seed_ratings)

class DatabaseTests(unittest.TestCase):
	"""Tests database-related functionality."""

	def setUp(self):
		"""Run before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

		# connect to test database
		connect_to_db(app, "postgresql:///testdb")

		# create tables
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

	def test_handle_login(self):
		"""Test handle-login route with user."""

		result = self.client.post("/handle-login",
								  data={'username': 'Octavia',
								  		'password': 'octaviapw'},
								  follow_redirects=True)

		with self.client as c:
			with c.session_transaction() as session:
				self.assertIn('username', session)

		self.assertEqual(result.status_code, 200)
		self.assertIn('Welcome back, Octavia!', result.data)
		self.assertIn('TOP PICKS FOR YOU', result.data)
		self.assertIn('Find', result.data)
		self.assertIn('Choose a city', result.data)
		self.assertIn('Log Out', result.data)
		self.assertNotIn('Sign Up', result.data)


	def test_handle_login_no_user(self):
		"""Test handle-login route without user."""

		result = self.client.post("/handle-login",
								  data={'username': 'NotInDatabase',
								  		'password': 'NotInDatabase'},
								  follow_redirects=True)

		self.assertEqual(result.status_code, 200)
		self.assertIn('Log In', result.data)
		self.assertIn('Email and/or password is invalid.', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Back to profile', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_signup_existing_user(self):
		"""Test handle-signup route with existing user."""

		result = self.client.post("/handle-signup",
									  data={'username': 'Octavia',
									  		'password': 'octaviapw'},
									  follow_redirects=True)

		self.assertIn('Account already exists. Please log in.', result.data)
	
	# best practice to split tests on conditional logic?
	def test_handle_signup_new_user(self):
		"""Test handle-signup route with new user."""

		result = self.client.post("/handle-signup",
								  data={'username': 'NewUser',
								  		'password': 'NewPassword'},
								  follow_redirects=True)

		# how to check if user in db?
		# assert db.session.query(User).filter_by(username='NewUser').one()

		self.assertIn('Account created! Please log in.', result.data)

	def test_profile_no_login(self):
		"""Test profile route with user not logged in."""

		result = self.client.get("/profile", follow_redirects=True)

		self.assertIn("Log in to see your profile", result.data)

	def test_search_logged_in(self):
		"""Test search route when user is logged in."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'
		
		result = self.client.get("/search")

		self.assertIn("Find", result.data)
		self.assertIn("Alameda", result.data)
		self.assertIn("Back to profile", result.data)

	def test_search_logged_out(self):
		"""Test search route when user is logged out."""

		result = self.client.get("/search")

		self.assertIn("Find", result.data)
		self.assertIn("Alameda", result.data)
		self.assertNotIn("Back to profile", result.data)

class UnitTests(unittest.TestCase):
	"""Test helper functions."""

	def setUp(self):
		"""Run before every test."""

		pass

	def tearDown(self):
		"""Run at the end of every test."""

		pass

class FlaskTests(unittest.TestCase):
	"""Test front-end functionality."""

	def setUp(self):
		"""Run before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

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
		self.assertIn('Log In', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_logout(self):
		"""Test handle-logout route."""

		result = self.client.get("/handle-logout", follow_redirects=True)
		self.assertIn('Log In', result.data)
		self.assertIn('Sign Up', result.data)

		with self.client as c:
			with c.session_transaction() as session:
				self.assertNotIn('username', session)

	def test_signup(self):
		"""Test signup route."""

		result = self.client.get("/signup")
		self.assertIn("Let's get you started!", result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)

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