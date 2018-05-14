import json
import csv
from model import *
# import pandas as pd

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
										  'yelp_rating': float(a.yelp_rating)}

	return rest_info

def create_row(columns_lst, rest_info, filename):
	"""Create a record for each restaurants, adding value to relevant columns."""

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

