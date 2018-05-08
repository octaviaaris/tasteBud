import json
from model import *

init_app()

def create_rest(filename):
	"""Import restaurants from data file."""

	with open(filename) as f:
		for line in f:
			line = json.loads(line)

			rest_id = line['id']
			name = line['name']
			url = line['url']
			address1 = line["location"]['address1']
			address2 = line["location"]['address2']
			address3 = line["location"]['address3']
			city = line["location"]['city']
			state = line["location"]['state']
			zipcode = line["location"]['zip_code']
			# latitude = line['coordinates']['latitude']
			# longitude = line['coordinates']['longitude']


			new = Restaurant(rest_id=rest_id,
							 name=name,
							 url=url,
							 address1=address1,
							 address2=address2,
							 address3=address3,
							 city=city,
							 state=state,
							 zipcode=zipcode,
							 # latitude=latitude,
							 # longitude=longitude,
							 hours=None,
							 price=None)

			db.session.add(new)

		db.session.commit()


def create_price():
	"""Populate price table."""

	one = Price(price_id=1)
	two = Price(price_id=2)
	three = Price(price_id=3)
	four = Price(price_id=4)

	db.session.add_all([one, two, three, four])
	db.session.commit()


def create_categories(filename):
	"""Import categories from data file."""

	aliases = []

	with open(filename) as f:
		for line in f:
			line = json.loads(line)
			categories = line['categories']
				
			for c in categories:
				alias = c['alias']

				if alias not in aliases:
					aliases.append(alias)
	
	print aliases

	for a in aliases:
		if not Category.query.filter_by(alias=a).all():
			new = Category(alias=a)
			db.session.add(new)

	db.session.commit()
