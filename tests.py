import unittest

from server import app
from model import (db,
				   connect_to_db,
				   example_users,
				   example_ratings,
				   delete_test_users,
				   delete_test_ratings,
				   User,
				   Restaurant)
from correlation import pearson
from recommender import show_top_picks, user_search_results
import json

class FlaskTests(unittest.TestCase):
	"""Test app functionality (no database)."""

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

	def test_signup(self):
		"""Test signup route."""

		result = self.client.get("/signup")
		self.assertIn("Let's get you started!", result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)

	def test_login(self):
		
		result = self.client.get("/login")
		self.assertIn("username", result.data)
		self.assertIn("password", result.data)

	def handle_logout(self):
		"""Test logout functionality."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/handle-logout", follow_redirects=True)

		with self.client as c:
			with c.session_transaction() as session:
				assert session == {}

		assertRedirects("/")
		self.assertIn("Log In", result.data)
		self.assertIn("Sign Up", result.data)

		self.assertNotIn("Back to profile", result.data)
		self.assertNotIn("Log out")

	def test_profile_loggged_in(self):
		"""Test profile route with user logged in."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'

		result = self.client.get("/profile")
		self.assertIn("tasteBud", result.data)
		self.assertIn("TOP PICKS FOR YOU", result.data)
		self.assertIn("Find Your Own", result.data)

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

		self.assertIn("Back to profile", result.data)
		self.assertIn("See your reviews", result.data)
		self.assertIn("Log out", result.data)

	def test_search_results_logged_out(self):
		"""Test search-results route (logged out)."""

		result = self.client.get("/search", follow_redirects=True)
		self.assertIn("Log in to find new eats", result.data)

	def test_details_logged_out(self):
		"""Test details route when user is not logged in."""

		result = self.client.get("/details/eYXwVR4mMAjzkJnm5wneHQ", follow_redirects=True)
		self.assertIn("Log in to review new restaurants", result.data)

	def test_details_logged_in(self):
		"""Test details route (logged in, unrated)."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'
				session['user_id'] = 1

		result = self.client.get("/details/eYXwVR4mMAjzkJnm5wneHQ")

		with self.client as c:
			with c.session_transaction() as session:
				assert (session['restaurant_id'] == 'eYXwVR4mMAjzkJnm5wneHQ')
	
	def test_reviews_logged_in(self):
		"""Test reviews route when user is not logged in."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'
				session['user_id'] = 1
				
		result = self.client.get("/reviews")
		self.assertIn("Back to profile", result.data)
		self.assertIn("Log out", result.data)
		
		self.assertNotIn("See your reviews", result.data)

	def test_reviews_logged_out(self):
		"""Test reviews route when user is not logged in."""

		result = self.client.get("/reviews", follow_redirects=True)
		self.assertIn("Log in to see your reviews", result.data)

class DatabaseTests(unittest.TestCase):
	"""Tests database-related app functionality."""

	def setUp(self):
		"""Run before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

		# connect to test database
		connect_to_db(app, "postgresql:///testdb")

		example_users()
		example_ratings()

	def tearDown(self):
		"""Run at the end of every test."""

		delete_test_ratings()
		delete_test_users()
		db.session.close()


	def test_handle_signup_new_user(self):
		"""Test handle-signup route with new user."""

		result = self.client.post("/handle-signup",
								  data={'username': 'NewUser',
								  		'password': 'NewPassword'},
								  follow_redirects=True)

		assert User.query.filter_by(username="NewUser").one()
		self.assertIn('Account created! Please log in.', result.data)

	def test_handle_signup_existing_user(self):
		"""Test handle-signup route with existing user."""

		result = self.client.post("/handle-signup",
								  data={'username': 'Octavia',
								  		'password': 'octaviapw'},
								  follow_redirects=True)

		assert User.query.filter_by(username="Octavia").one()
		self.assertIn('Account already exists. Please log in.', result.data)
	
	def test_handle_login(self):
		"""Test handle-login route with existing user."""

		result = self.client.post("/handle-login",
								  data={'username': 'Octavia',
								  		'password': 'octaviapw'},
								  follow_redirects=True)

		with self.client as c:
			with c.session_transaction() as session:
				self.assertIn('username', session)

		assert (User.query.filter_by(username="Octavia").one() != None)
		self.assertIn('Welcome back, Octavia!', result.data)
		self.assertIn('TOP PICKS FOR YOU', result.data)
		self.assertIn('Log out', result.data)
		self.assertNotIn('Sign Up', result.data)

	def test_handle_login_no_user(self):
		"""Test handle-login route without user."""

		result = self.client.post("/handle-login",
								  data={'username': 'NotInDatabase',
								  		'password': 'NotInDatabase'},
								  follow_redirects=True)

		assert (User.query.filter_by(username="NotInDatabase").first() == None)
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

		assert (User.query.filter_by(username="Octavia").one().password != "WrongPassword")
		self.assertIn('Log In', result.data)
		self.assertIn('Email and/or password is invalid.', result.data)
		self.assertIn('username', result.data)
		self.assertIn('password', result.data)
		self.assertNotIn('Back to profile', result.data)
		self.assertNotIn('Sign Up', result.data)

	

	# def test_search_results_logged_in(self):
	# 	"""Test search-results route (logged in)."""

	# 	with self.client as c:
	# 		with c.session_transaction() as session:
	# 			session['username'] = 'Octavia'

	# 	result = self.client.get("/search-results",
	# 							 query_string={'city': 'Oakland'})

	# 	self.assertIn("Back to profile", result.data)
	# 	self.assertIn("Restaurants in Oakland", result.data)
	# 	self.assertIn("Cholita Linda (2)", result.data)

	# jasmine test
	# def test_details_logged_in(self):
	# 	"""Test details route (logged in)."""

	# 	with self.client as c:
	# 		with c.session_transaction() as session:
	# 			session['username'] = 'Octavia'
	# 			session['user_id'] = 1

	# 	result = self.client.get("/details/UHFjEP5dVn4wqcjt7ByUog",
	# 							 query_string={'restaurant_id': 'UHFjEP5dVn4wqcjt7ByUog'})

	# 	self.assertIn("Back to profile", result.data)
	# 	self.assertIn("Cholita Linda", result.data)
	# 	self.assertIn("Price", result.data)
	# 	self.assertIn("Yelp Rating", result.data)
	# 	self.assertIn("Your rating", result.data)
	# 	self.assertIn("Go to yelp page", result.data)

	# jasmine test
	
	def test_rate_restaurant_new(self):
		"""Test rate-restaurant route new rating."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'
				octavia = User.query.filter_by(username="Octavia").one()
				session['user_id'] = octavia.user_id
				session["restaurant_id"] = 'YH82tozaJi_cCKU6xF6IxQ'

		result = self.client.get("/rate-restaurant.json?rating=4")

		self.assertEqual(result.status_code, 200)
		self.assertIn('{\n  "rating": 4.0\n}', result.data)

	def test_rate_restaurant_overwrite(self):
		"""Test rate-restaurant route, overwrite existing rating."""

		with self.client as c:
			with c.session_transaction() as session:
				session['username'] = 'Octavia'
				octavia = User.query.filter_by(username="Octavia").one()
				session['user_id'] = octavia.user_id
				session["restaurant_id"] = '1048yN4bQRt_h3zQ04GDSA'

		result = self.client.get("/rate-restaurant.json?rating=4")

		self.assertEqual(result.status_code, 200)
		self.assertIn('{\n  "rating": 4.0\n}', result.data)

	def test_cities_json(self):
		"""Test cities.json route."""

		# result.data not same as what's actually returned
		result = self.client.get("/cities.json")
		self.assertIn("Oakland", result.data)
		pass

	def test_top_picks(self):
		"""Test top-picks.json route."""

		result = self.client.get("/search.json?search_string=greek&city=Oakland")
		pass

	def test_details(self):
		"""Test details.json route."""

		pass

	def test_rate_restaurant(self):
		"""Test rate-restaurant.json route."""

		pass

	def test_user_rating(self):
		"""Test user-rating.json route."""

		pass

	def test_reviews_json(self):
		"""Test reviews.json route."""

		pass

class UnitTests(unittest.TestCase):
	"""Test helper functions."""

	def setUp(self):
		"""Run before every test."""

		connect_to_db(app, "postgresql:///testdb")


	def tearDown(self):
		"""Run at the end of every test."""

		# delete_test_users()
		db.session.close()

	def test_pearson(self):
		"""Test pearson function."""

		pairs_1 = [(1.0, 1.0), (3.0, 3.0), (4.0, 4.0), (2.0, 2.0)]
		pairs_2 = [(1.0, 5.0), (3.0, 3.0), (1.0, 4.0), (3.0, 2.0)]
		pairs_3 = [(1.0, 2.0), (3.0, 3.0), (1.0, 1.0), (3.0, 2.0)]
		pairs_4 = [(0.0, 5.0), (0.0, 2.0), (0.0, 1.0), (0.0, 3.0)]

		self.assertEqual(pearson(pairs_1), 1.0)
		self.assertEqual(pearson(pairs_2), -0.8944271909999159)
		self.assertEqual(pearson(pairs_3), 0.7071067811865475)
		self.assertEqual(pearson(pairs_4), 0)

	def test_show_top_picks(self):
		"""Test show_top_picks function."""

		user = User(username="NewUser", password="NewPassword")

		show_top_picks(user)

	def test_user_search_results(self):
		"""Test user_search_results function."""

		self.assertIsNotNone(user_search_results("Oakland", "greek"))
		self.assertIsNotNone(user_search_results("San Francisco", "japanese asian"))
		self.assertIsNotNone(user_search_results("San Francisco", "japanese, chinese, korean"))

class DatabaseSeedTests(unittest.TestCase):
	"""Test proper seeding."""

	def setUp(self):
		"""Run before every test."""

		app.config['TESTING'] = True
		app.config['SECRET_KEY'] = 'key'
		self.client = app.test_client()

	def tearDown(self):
		"""Run at the end of every test."""

		pass

	def test_connect_to_db(self):
		
		pass


if __name__ == "__main__":
	unittest.main()

