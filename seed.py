import json
from model import *

init_app()

def seed_restaurants(filename):
	"""Import restaurants (minus price and yelp_ratings) from data file."""

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


def seed_categories(filename):
	"""Import categories from data file."""

	aliases = []

	with open(filename) as f:
		for line in f:
			line = json.loads(line)
			categories = line['categories']
			
			for c in categories:
				alias = c['alias']

				# ensure no duplicates
				if alias not in aliases:
					aliases.append(alias)

	# add all items in aliases list not already in db
	for a in aliases:
		if not Category.query.filter_by(category=a).all():
			new = Category(category=a)
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
	"""Populate rest_cats table."""

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

