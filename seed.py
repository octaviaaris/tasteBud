import json
from model import *

init_app()

def seed_restaurants(filename):
	"""Import restaurants (minus price and yelp_ratings) from data file.
	Use all_restaurants.txt (or sf_data.txt and oak_data.txt)."""

	with open(filename) as f:
		for line in f:
			line = json.loads(line)

			restaurant_id = line['id']
			name = line['name']
			url = line['url']
			address1 = line['location']['address1']
			address2 = line['location']['address2']
			address3 = line['location']['address3']
			city = line['location']['city']
			state = line['location']['state']
			zipcode = line['location']['zip_code']
			latitude = line['coordinates']['latitude']
			longitude = line['coordinates']['longitude']

			new = Restaurant(restaurant_id=restaurant_id,
							 name=name,
							 url=url,
							 address1=address1,
							 address2=address2,
							 address3=address3,
							 city=city,
							 state=state,
							 zipcode=zipcode,
							 latitude=latitude,
							 longitude=longitude,
							 hours=None,
							 price=None,
							 yelp_rating=None)

			if not Restaurant.query.filter_by(restaurant_id=restaurant_id).all():
				db.session.add(new)

		db.session.commit()

def seed_price_ratings(filename):
	"""Populate price and rating data for each restaurant from price_ratings.txt."""

	with open(filename, 'r') as f:
		line = f.read()
		seed_dct = json.loads(line)

	all_restaurants = Restaurant.query.all()

	for a in all_restaurants:
		a.price = seed_dct[a.restaurant_id]['price']
		a.yelp_rating = seed_dct[a.restaurant_id]['yelp_rating']

		db.session.commit()

def seed_categories(filename):
	"""Import categories from data file. Use categories.txt."""

	with open(filename) as f:
		for line in f:
			line = line.strip()
			new = Category(category=line)
			db.session.add(new)

	db.session.commit()

def seed_prices():
	"""Populate price table."""

	one = Price(price=1)
	two = Price(price=2)
	three = Price(price=3)
	four = Price(price=4)

	db.session.add_all([one, two, three, four])
	db.session.commit()

def seed_rest_cats(filename):
	"""Populate rest_cats table. 
	Use all_restaurants.txt (or sf_data.txt and oak_data.txt)."""

	with open(filename) as f:
		for line in f:
			line = json.loads(line)
			restaurant_id = line['id']
			categories = line['categories']

			for c in categories:
				alias = c['alias']

				new = Rest_cat(restaurant_id=restaurant_id,
							   category=alias)
				db.session.add(new)

	db.session.commit()

def seed_users(filename):
	"""Populate users table.
	Use users.csv"""

	with open(filename) as f:
		for line in f:
			line = line.split(",")
			username = str(line[0].strip())
			password = str(line[1].strip())

			new = User(username=username,
					   password=password,
					   score_avg=None)

			db.session.add(new)

	db.session.commit()

def seed_ratings(filename):
	"""Populate ratings table.
	Use ratings.csv."""

	with open(filename) as f:
		for line in f:
			line = line.strip().split(",")
			restaurant_id = line[0]
			user_id = line[1]
			user_rating = line[2]

			new = Rating(restaurant_id=restaurant_id,
						 user_id=user_id,
						 user_rating=user_rating)

			db.session.add(new)

	db.session.commit()


if __name__ == "__main__":

	seed_prices()
	seed_categories('database/categories.txt')
	seed_restaurants('database/all_restaurants.txt')
	seed_price_ratings('database/price_ratings.txt')
	seed_rest_cats('database/all_restaurants.txt')
	seed_users('database/users.csv')
	seed_ratings('database/ratings.csv')
