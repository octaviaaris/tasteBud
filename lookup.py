
###############################################################
############# lookup dictionaries for recommender #############
###############################################################

import json

with open('database/restaurants_to_categories.json', 'r') as f:
	rtc = json.loads(f.read())

with open('database/categories_to_restaurants.json', 'r') as f:
	ctr = json.loads(f.read())
	
with open('database/price_ratings.txt', 'r') as f:
	rp = json.loads(f.read()) 