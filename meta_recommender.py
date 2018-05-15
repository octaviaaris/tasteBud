import json
import csv
from model import *

init_app()

def make_columns():
	"""Return list of each unique category plus price and yelp_rating to be used as column names in csv."""

	all_cats = ['id']
	all_cats = all_cats + [c.category for c in Category.query.all()]
	all_cats = all_cats + ['price', 'yelp_rating']
	
	return all_cats

def get_restaurants_info():
	"""Return dictionary of restaurants and their categories, price and yelp_rating.

		{id: 
			{categories: [], 
			 price: 2, 
			 yelp_rating: 2}
		}

	"""

	all_restaurants = Restaurant.query.all()

	rest_info = {}
	for a in all_restaurants:
		# remove duplicate categories (find out why there are duplicates)
		rest_info[a.restaurant_id] = {'categories': list(set([r.category for r in a.rest_cats])),
										  'price': a.price,
										  'yelp_rating': a.yelp_rating}

	return rest_info

def create_row(columns_lst, rest_info, filename):
	"""Create a record for each restaurant, adding value to relevant columns."""
	
	with open(filename, 'a+') as f:
		rowwriter = csv.writer(f)
		for r in rest_info:
			row = [r]
			tick = [columns_lst.index(c) for c in rest_info[r]['categories']]
			tick.sort()

			for i in range(1,len(columns_lst)-2):
				if i in tick:
					row.append(1)
				else:
					row.append(0)

			row = row + [rest_info[r]['price'], rest_info[r]['yelp_rating']]
			rowwriter.writerow(row)

def encode_restaurants(columns_lst, rest_info):
	"""Create dictionary of restaurant_id keys and list of encoded categories, price and yelp_rating."""

	rest_info = get_restaurants_info()
	encoded_restaurants = {}

	# compare every combination of two restaurants (iterate through rows to find matching rows)
	# tally up the number of matches
	# for each restaurant, choose top ten restaurants with highest tallies

	for r in rest_info:
		row = [r]
		tick = [columns_lst.index(c) for c in rest_info[r]['categories']]
		tick.sort()

		for i in range(1,len(columns_lst)-2):
			if i in tick:
				row.append(1)
			else:
				row.append(0)

		row = row + [rest_info[r]['price'], rest_info[r]['yelp_rating']]
		rowwriter.writerow(row)


def find_sim_restaurants(restaurant_id):
	"""Compares restaurant to all other restaurants in database and counts match score (based on attribute)."""

	matches = []
	anchor = Restaurant.query.get(restaurant_id)
	anchor_attributes = anchor.get_attributes()
	other_restaurants = Restaurant.query.filter(Restaurant.restaurant_id != restaurant_id)

	for r in other_restaurants:
		other_attributes = r.get_attributes()
		match_score = 0.0

		for c in anchor_attributes['categories']:
			if c in other_attributes['categories']:
				match_score += 1

		# if anchor_attributes['price'] == other_attributes['price']:
		# 	match_score += 1

		# if anchor_attributes['yelp_rating'] == other_attributes['yelp_rating']:
		# 	match_score += 1

		# divide category match score by total possible points (number of anchor's categories + number of other's categories)
		match_score /= len(set(anchor_attributes['categories'] + other_attributes['categories']))

		matches.append((match_score, r))

	matches.sort(reverse=True)

	# save only restaurants with 4 or 5 stars
	top_matches = []

	for m in matches:
		if m[1].yelp_rating > 3:
			top_matches.append(m)

	top_matches = top_matches[:10]

	return top_matches

