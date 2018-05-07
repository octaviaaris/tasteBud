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
HEADER = {
	'Authorization': 'Bearer {key}'.format(key=API_KEY)	
}



def search_businesses(location, offset=0):
	"""Get business ids for specified location."""

	url = API_HOST + SEARCH_PATH

	params = {"term": ["restaurant"],
			  "location": location,
			  "offset": offset}

	response = requests.request('GET', url, headers=HEADER, params=params)

	result = response.json()

	businesses = result['businesses']

	for b in businesses:
		print b

	with open('rest_data.txt', 'a') as f:
		for b in businesses:
			f.write(json.dumps(b))
			f.write("\n")


