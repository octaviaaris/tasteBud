from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import os
import requests
import json
import csv
from model import *

init_app()


############################################################################################################
############################################# Yelp API requests ############################################
############################################################################################################

API_KEY = os.environ['YELP_API_KEY']

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
HEADER = {'Authorization': 'Bearer {key}'.format(key=API_KEY)}


def search_businesses(location, filename, offset=0):
	"""Get info about businesses from specified location.
	
	-setting term to restaurant filters out non-food businesses
	-offset gets the next batch to avoid repeats
	-limit specifies how many results to return with each query

	"""

	url = API_HOST + SEARCH_PATH

	params = {"term": "restaurant",
			  "location": location,
			  "offset": offset,
			  "limit": 50}

	response = requests.request("GET", url, headers=HEADER, params=params)

	result = response.json()

	businesses = result["businesses"]

	with open(filename, "a+") as f:
		string = f.read()
		for b in businesses:
			# ensure entry is not a repeat
			if b['id'] not in string:
				f.write(json.dumps(b))
				f.write("\n")


def get_sf(filename):
	"""Get 1000 restaurants in SF."""

	offset = 0

	while offset < 951:
		search_businesses('San Francisco', filename, offset)
		offset += 50

	return "Done!"


def get_oak(filename):
	"""Get 1000 restaurants in Oakland."""

	offset = 0

	while offset < 951:
		search_businesses('Oakland', filename, offset)
		offset += 50

	return "Done!"


def restaurant_price_and_rating(restaurants):
	"""Get prices for each restaurant in a list of restaurant objects."""

	# restaurants = Restaurant.query.all()
	
	for rst in restaurants:

		url = API_HOST + BUSINESS_PATH + rst.restaurant_id
		response = requests.request("GET", url, headers=HEADER)
		r = response.json()

		price = r.get('price', None)
		if price:
			price = len(price)
		yelp_rating = r.get('rating', None)

		rst.price = price
		rst.yelp_rating = yelp_rating

		db.session.commit()

	return "Done!"

############################################################################################################
#################################### Save db to files for easy reseeding ###################################
############################################################################################################

def save_price_rating():
	"""Save price and yelp_rating data for each restaurant to txt file for easy reseeding."""

	all_restaurants = Restaurant.query.all()

	price_rating = {}

	for a in all_restaurants:
		price_rating[a.restaurant_id] = {'price': a.price, 'yelp_rating': float(a.yelp_rating)}

	with open('database/ratings_prices.txt', 'a+') as f:
		f.write(json.dumps(price_rating))

	return price_rating

def save_categories():
	"""Save current categories in database to categories.txt for easy reseeding."""

	categories = Category.query.all()

	with open('database/categories.txt', 'w') as f:
		for c in categories:
			f.write(c.category)
			f.write("\n")

def save_users():
	"""Save current users in database to users.csv."""

	users = User.query.all()

	with open('database/users.csv', 'a+') as f:
		rowwriter = csv.writer(f)
		for u in users:
			row = [u.user_id, u.username, u.password, u.score_avg]
			rowwriter.writerow(row)

def save_ratings():
	"""Save current ratings in database to ratings.csv."""

	ratings = Rating.query.all()

	with open('database/ratings.csv', 'a+') as f:
		rowwriter = csv.writer(f)
		header = ['rating_id', 'restaurant_id', 'user_id', 'user_rating']
		rowwriter.writerow(header)
		for r in ratings:
			row = [r.rating_id, r.restaurant_id, r.user_id, r.user_rating]
			rowwriter.writerow(row)

def restaurants_to_categories():
	"""Create JSON file of restaurant_id: {categories} key, value pairs."""

	rtc_dict = {}
	all_restaurants = Restaurant.query.options(db.joinedload('rest_cats').joinedload('categories')).all()
	
	for r in all_restaurants:
		categories = [rc.categories.category for rc in r.rest_cats]
		rtc_dict[r.restaurant_id] = categories

	with open('database/restaurants_to_categories.json', 'w') as f:
		f.write(json.dumps(rtc_dict))

def categories_to_restaurants():
	"""Create JSON file of category: {restaurant_id} key value pairs."""

	ctr_dict = {}
	all_categories = Category.query.options(db.joinedload('rest_cats').joinedload('categories')).all()

	for c in all_categories:
		restaurants = [rc.restaurants.restaurant_id for rc in c.rest_cats]
		ctr_dict[c.category] = restaurants

	with open('database/categories_to_restaurants.json', 'w') as f:
		f.write(json.dumps(ctr_dict))



