from server import app
from model import db, connect_to_db, example_users, example_ratings
from seed import (seed_prices,
				  seed_categories,
				  seed_restaurants,
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
	seed_restaurants('database/restaurant_subset.txt')
	seed_rest_cats('database/restaurant_subset.txt')
	seed_users('database/users.csv')
	seed_ratings('database/ratings.csv')