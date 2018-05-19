import unittest

from server import app
from model import db, connect_to_db, example_users, example_ratings
from seed import (seed_users,
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

		# seed ratings, users, example ratings, example users

	def tearDown(self):
		"""Run at the end of every test."""

		db.session.close()
		# figure out how to delete users and ratings for logged_in_unrated and 


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

	def test_search_results_logged_in(self):
		"""Test search-results route (logged in)."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/search-results",
								 query_string={'location': 'Oakland'})

		self.assertIn("Back to profile", result.data)
		self.assertIn("Restaurants in Oakland", result.data)
		self.assertIn("Cholita Linda", result.data)

	def test_search_results_logged_out(self):
		"""Test search-results route (logged out)."""

		result = self.client.get("/search-results",
								 query_string={'location': 'Oakland'})


		self.assertIn("Restaurants in Oakland", result.data)
		self.assertIn("Cholita Linda", result.data)

		self.assertNotIn("Back to profile", result.data)

	def test_details_logged_in(self):
		"""Test details route (logged in)."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/details/UHFjEP5dVn4wqcjt7ByUog",
								 query_string={'restaurant_id': 'UHFjEP5dVn4wqcjt7ByUog'})

		self.assertIn("Back to profile", result.data)
		self.assertIn("Cholita Linda", result.data)
		self.assertIn("Price", result.data)
		self.assertIn("Yelp Rating", result.data)
		self.assertIn("Your rating", result.data)
		self.assertIn("Go to yelp page", result.data)

	def test_details_logged_in_unrated(self):
		"""Test details route (logged in, unrated)."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/details/PkLfjhJ_XExjwARO1RkQIw",
								 query_string={'restaurant_id': 'PkLfjhJ_XExjwARO1RkQIw'})

		self.assertIn("Back to profile", result.data)
		self.assertIn("Bakesale Betty", result.data)
		self.assertIn("Price", result.data)
		self.assertIn("Yelp Rating", result.data)
		self.assertIn("Tell us what you think", result.data)
		self.assertIn("Go to yelp page", result.data)
		self.assertNotIn("Your rating", result.data)

	def test_details_logged_out(self):
		"""Test details route (logged out)."""

		result = self.client.get("/details/UHFjEP5dVn4wqcjt7ByUog",
								 query_string={'restaurant_id': 'UHFjEP5dVn4wqcjt7ByUog'})

		self.assertIn("Cholita Linda", result.data)
		self.assertIn("Price", result.data)
		self.assertIn("Yelp Rating", result.data)
		self.assertIn("Go to yelp page", result.data)

		self.assertNotIn("Back to profile", result.data)
		self.assertNotIn("Your rating", result.data)

	def test_rate_restaurant_new(self):
		"""Test rate-restaurant route new rating."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.post("/rate-restaurant",
								 data={'rating': '4',
								 	   'restaurant_id': 'eYXwVR4mMAjzkJnm5wneHQ'},
								 follow_redirects=True)

		self.assertEqual(result.status_code, 200)
		self.assertIn("Your rating: 4.0", result.data)


	def test_rate_restaurant_overwrite(self):
		"""Test rate-restaurant route, overwrite existing rating."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.post("/rate-restaurant",
								 data={'rating': '4',
								 	   'restaurant_id': '1048yN4bQRt_h3zQ04GDSA'},
								 follow_redirects=True)

		self.assertEqual(result.status_code, 200)
		self.assertIn("East Ocean Seafood Restaurant", result.data)
		self.assertIn("Your rating: 4.0", result.data)


class LoginSignUpTests(unittest.TestCase):
	"""Test login/logout and signup functionality."""

	def setUp(self):
		"""Run before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

		# connect to test database
		connect_to_db(app, "postgresql:///usersdb")
		db.create_all()
		example_users()

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

		self.assertIn('Log In', result.data)
		self.assertIn('Email and/or password is invalid.', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Back to profile', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_login_invalid(self):
		"""Test handle-login route with mismatch user credentials."""

		result = self.client.post("/handle-login",
								  data={'username': 'Octavia',
								  		'password': 'WrongPassword'},
								  follow_redirects=True)

		self.assertIn('Log In', result.data)
		self.assertIn('Email and/or password is invalid.', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Back to profile', result.data)
		self.assertNotIn('Sign Up', result.data)

	def handle_logout(self):
		"""Test logout functionality."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/handle-logout", follow_redirects=True)

		with self.client as c:
			with c.session_transaction() as session:
				self.assertNotIn('username', session)

		self.assertEqual(result.status_code, 200)
		self.assertIn("Log In", result.data)
		self.assertIn("Sign Up", result.data)

		self.assertNotIn("Back to profile", result.data)
		self.assertNotIn("Log Out")

	def test_signup(self):
		"""Test signup route."""

		result = self.client.get("/signup")
		self.assertIn("Let's get you started!", result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)

	def test_handle_signup_new_user(self):
		"""Test handle-signup route with new user."""

		result = self.client.post("/handle-signup",
								  data={'username': 'NewUser',
								  		'password': 'NewPassword'},
								  follow_redirects=True)

		self.assertIn('Account created! Please log in.', result.data)

	def test_handle_signup_existing_user(self):
		"""Test handle-signup route with existing user."""

		result = self.client.post("/handle-signup",
									  data={'username': 'Octavia',
									  		'password': 'octaviapw'},
									  follow_redirects=True)

		self.assertIn('Account already exists. Please log in.', result.data)

	# def test_rate_restaurant_overwrite(self):
	# 	"""Test rate-restaurant route."""

	# 	with self.client as c:
	# 		with c.session_transaction() as session:
	# 			session['username'] = 'Octavia'

	# 	result = self.client.post("/rate-restaurant",
	# 							 data={'rating': '4',
	# 							 	   'restaurant_id': 'gQMpKljmisp-wDT5W0OOTA'},
	# 							 follow_redirects=True)

	# 	self.assertEqual(result.status_code, 200)
	# 	self.assertIn("Mae Krua", result.data)
	# 	self.assertIn("Your rating: 4.0", result.data)

class UnitTests(unittest.TestCase):
	"""Test helper functions."""

	def setUp(self):
		"""Run before every test."""

		pass

	def tearDown(self):
		"""Run at the end of every test."""

		pass

class FlaskTests(unittest.TestCase):
	"""Test front-end functionality (no database)."""

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
























if __name__ == "__main__":
	unittest.main()