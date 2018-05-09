from urllib2 import HTTPError
from urllib import quote
from urllib import urlencode
import os
import requests
import json

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

	url = "https://api.yelp.com/v3/businesses/search"

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


def restaurant_price_and_rating():
	"""Get prices for each restaurant."""

	all_restaurants = Restaurant.query.all()

	i = 1

	for a in all_restaurants:
		print "{i}: {id}".format(i=i, id=a.restaurant_id)
		i += 1

		# query Yelp using business ID
