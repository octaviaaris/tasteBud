from server import app
from model import db, connect_to_db, example_users, example_ratings
from seed import (seed_prices,
				  seed_categories,
				  seed_restaurants,
				  seed_price_ratings,
				  seed_rest_cats,
				  seed_users,
				  seed_ratings)

def seed_testdb():
	connect_to_db(app, 'postgres:///testdb')

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

def seed_usersdb():

	connect_to_db(app, 'postgres:///usersdb')

	# create tables
	db.create_all()
